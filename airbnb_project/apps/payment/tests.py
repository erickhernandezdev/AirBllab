from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from apps.core.models import (
    Accommodation,
    AccommodationType,
    Activity,
    ActivityType,
    Cart,
    CartActivity,
    CartService,
    CustomUser,
    Service,
    ServiceType,
)


class PaymentTestBase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            name="Test User",
            role="USER",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel",
            description="Hotel test",
        )

        self.service_type = ServiceType.objects.create(
            name="Spa",
            description="Spa test",
        )

        self.activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour test",
        )

        self.accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Test Hotel",
            description="Hotel de prueba",
            location="San José",
            price=50000,
            rating=4.5,
            status="Aprobado",
        )

        self.service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Test Spa",
            description="Spa de prueba",
            price=15000,
            rating=4.5,
            status="Aprobado",
        )

        self.activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Test Tour",
            description="Tour de prueba",
            location="Cartago",
            price=20000,
            rating=4.5,
            status="Aprobado",
        )

        self.url = reverse("checkout-stripe")


class PaymentAccessTest(PaymentTestBase):
    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)


class StripeCheckoutTest(PaymentTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_empty_cart_redirects_to_cart(self, mock_create):
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            "http://127.0.0.1:8000/cart/?empty=true",
            fetch_redirect_response=False,
        )

        mock_create.assert_not_called()

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_accommodation_is_added_to_line_items(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "https://checkout.stripe.com/test",
        )

        mock_create.assert_called_once()

        kwargs = mock_create.call_args.kwargs
        line_items = kwargs["line_items"]

        self.assertEqual(len(line_items), 1)

        self.assertEqual(
            line_items[0]["price_data"]["currency"],
            "crc",
        )

        self.assertEqual(
            line_items[0]["price_data"]["unit_amount"],
            5000000,
        )

        self.assertEqual(
            line_items[0]["price_data"]["product_data"]["name"],
            "Alojamiento: Test Hotel",
        )

        self.assertEqual(
            line_items[0]["quantity"],
            1,
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_service_is_added_to_line_items(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        cart = Cart.objects.create(user=self.user)

        CartService.objects.create(
            cart=cart,
            service=self.service,
            total_price=15000,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        kwargs = mock_create.call_args.kwargs
        line_items = kwargs["line_items"]

        self.assertEqual(len(line_items), 1)

        self.assertEqual(
            line_items[0]["price_data"]["unit_amount"],
            1500000,
        )

        self.assertEqual(
            line_items[0]["price_data"]["product_data"]["name"],
            "Servicio: Test Spa",
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_activity_is_added_to_line_items(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        cart = Cart.objects.create(user=self.user)

        CartActivity.objects.create(
            cart=cart,
            activity=self.activity,
            total_price=20000,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        kwargs = mock_create.call_args.kwargs
        line_items = kwargs["line_items"]

        self.assertEqual(len(line_items), 1)

        self.assertEqual(
            line_items[0]["price_data"]["unit_amount"],
            2000000,
        )

        self.assertEqual(
            line_items[0]["price_data"]["product_data"]["name"],
            "Actividad: Test Tour",
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_all_cart_items_are_added(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        cart = Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        CartService.objects.create(
            cart=cart,
            service=self.service,
            total_price=15000,
        )

        CartActivity.objects.create(
            cart=cart,
            activity=self.activity,
            total_price=20000,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)

        kwargs = mock_create.call_args.kwargs

        self.assertEqual(
            len(kwargs["line_items"]),
            3,
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_checkout_uses_payment_mode(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        self.client.post(self.url)

        kwargs = mock_create.call_args.kwargs

        self.assertEqual(
            kwargs["payment_method_types"],
            ["card"],
        )

        self.assertEqual(
            kwargs["mode"],
            "payment",
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_checkout_contains_correct_user_reference(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        self.client.post(self.url)

        kwargs = mock_create.call_args.kwargs

        self.assertEqual(
            kwargs["client_reference_id"],
            str(self.user.pk),
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_checkout_contains_success_and_cancel_urls(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        self.client.post(self.url)

        kwargs = mock_create.call_args.kwargs

        self.assertEqual(
            kwargs["success_url"],
            "http://127.0.0.1:8000/cart/?success=true",
        )

        self.assertEqual(
            kwargs["cancel_url"],
            "http://127.0.0.1:8000/cart/?canceled=true",
        )

    @patch("apps.payment.views.stripe.checkout.Session.create")
    def test_checkout_redirects_to_stripe(self, mock_create):
        mock_create.return_value.url = "https://checkout.stripe.com/test"

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            price_total=50000,
        )

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "https://checkout.stripe.com/test",
        )
