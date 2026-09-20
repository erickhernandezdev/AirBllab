from datetime import date
from decimal import Decimal
from urllib.parse import unquote

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
    Invoice,
    InvoiceItem,
    Reservation,
    ReservationActivity,
    ReservationService,
    Service,
    ServiceType,
)

from .views import expiry_valid, luhn_check


class CartHelpersTest(TestCase):
    def test_luhn_accepts_valid_card(self):
        self.assertTrue(luhn_check("4111111111111111"))

    def test_luhn_rejects_invalid_card(self):
        self.assertFalse(luhn_check("4111111111111112"))

    def test_expiry_accepts_future_date(self):
        self.assertTrue(expiry_valid("12/99"))

    def test_expiry_rejects_invalid_month(self):
        self.assertFalse(expiry_valid("13/99"))

    def test_expiry_rejects_invalid_format(self):
        self.assertFalse(expiry_valid("invalid"))

    def test_expiry_rejects_empty_value(self):
        self.assertFalse(expiry_valid(""))

    def test_expiry_rejects_expired_card(self):
        self.assertFalse(expiry_valid("01/20"))


class CartViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="Test User",
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("cart"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_authenticated_user_can_access_cart(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("cart"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart/cart.html")

    def test_empty_cart_does_not_include_cart_data(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("cart"))

        self.assertNotIn("cart", response.context)

    def test_cart_context_contains_totals(self):
        cart = Cart.objects.create(
            user=self.user,
            nights=2,
            price_total=100000,
        )

        activity_type = ActivityType.objects.create(name="Tour")
        service_type = ServiceType.objects.create(name="Transporte")

        activity = Activity.objects.create(
            host=self.user,
            activity_type=activity_type,
            name="Tour",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        service = Service.objects.create(
            host=self.user,
            service_type=service_type,
            name="Transporte",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        CartActivity.objects.create(
            cart=cart,
            activity=activity,
            total_price=Decimal("20000.00"),
            date=date(2026, 10, 1),
        )

        CartService.objects.create(
            cart=cart,
            service=service,
            total_price=Decimal("15000.00"),
            date=date(2026, 10, 1),
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse("cart"))

        self.assertEqual(response.context["total_accommodation"], 100000)
        self.assertEqual(response.context["total_activities"], 20000)
        self.assertEqual(response.context["total_services"], 15000)
        self.assertEqual(response.context["grand_total"], 135000)

    def test_cart_displays_message_from_query_string(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("cart") + "?message=Test%20message")

        self.assertEqual(
            response.context["message"],
            "Test message",
        )


class AddToCartViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="Test User",
        )

        self.accommodation_type = AccommodationType.objects.create(name="Hotel")

        self.activity_type = ActivityType.objects.create(name="Tour")

        self.service_type = ServiceType.objects.create(name="Transporte")

        self.accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
        )

        self.activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Tour Test",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        self.service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Servicio Test",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        self.client.force_login(self.user)

    def test_add_accommodation_to_cart(self):
        response = self.client.post(
            reverse("add_to_cart"),
            {
                "accommodation_id": self.accommodation.id,
                "start_date": "2026-10-01",
                "end_date": "2026-10-05",
                "nights": "4",
                "price_total": "200000",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

        cart = Cart.objects.get(user=self.user)

        self.assertEqual(
            cart.accommodation_id,
            self.accommodation.id,
        )
        self.assertEqual(cart.nights, 4)
        self.assertEqual(cart.price_total, 200000)

    def test_cannot_add_second_accommodation(self):
        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
        )

        response = self.client.post(
            reverse("add_to_cart"),
            {
                "accommodation_id": self.accommodation.id,
                "start_date": "2026-10-01",
                "end_date": "2026-10-05",
                "nights": "4",
                "price_total": "200000",
            },
        )

        self.assertEqual(response.json()["status"], "error")

    def test_add_service_to_cart(self):
        response = self.client.post(
            reverse("add_to_cart"),
            {
                "service_id": self.service.id,
                "total_price": "15000.00",
                "date": "2026-10-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(
            CartService.objects.filter(
                cart__user=self.user,
                service=self.service,
            ).count(),
            1,
        )

    def test_cannot_add_same_service_twice(self):
        cart = Cart.objects.create(user=self.user)

        CartService.objects.create(
            cart=cart,
            service=self.service,
            total_price=Decimal("15000.00"),
            date=date(2026, 10, 1),
        )

        response = self.client.post(
            reverse("add_to_cart"),
            {
                "service_id": self.service.id,
                "total_price": "15000.00",
                "date": "2026-10-01",
            },
        )

        self.assertEqual(response.json()["status"], "error")

    def test_add_activity_to_cart(self):
        response = self.client.post(
            reverse("add_to_cart"),
            {
                "activity_id": self.activity.id,
                "total_price": "20000.00",
                "date": "2026-10-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(
            CartActivity.objects.filter(
                cart__user=self.user,
                activity=self.activity,
            ).count(),
            1,
        )

    def test_cannot_add_same_activity_twice(self):
        cart = Cart.objects.create(user=self.user)

        CartActivity.objects.create(
            cart=cart,
            activity=self.activity,
            total_price=Decimal("20000.00"),
            date=date(2026, 10, 1),
        )

        response = self.client.post(
            reverse("add_to_cart"),
            {
                "activity_id": self.activity.id,
                "total_price": "20000.00",
                "date": "2026-10-01",
            },
        )

        self.assertEqual(response.json()["status"], "error")


class ClearCartViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        self.cart = Cart.objects.create(
            user=self.user,
            nights=3,
            price_total=150000,
        )

        activity_type = ActivityType.objects.create(name="Tour")
        service_type = ServiceType.objects.create(name="Servicio")

        activity = Activity.objects.create(
            host=self.user,
            activity_type=activity_type,
            name="Tour",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        service = Service.objects.create(
            host=self.user,
            service_type=service_type,
            name="Servicio",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        CartActivity.objects.create(
            cart=self.cart,
            activity=activity,
            total_price=Decimal("20000.00"),
        )

        CartService.objects.create(
            cart=self.cart,
            service=service,
            total_price=Decimal("15000.00"),
        )

        self.client.force_login(self.user)

    def test_clear_cart_removes_all_items(self):
        response = self.client.post(reverse("clear_cart"))

        self.assertRedirects(response, reverse("cart"))

        self.assertEqual(
            CartActivity.objects.filter(cart=self.cart).count(),
            0,
        )
        self.assertEqual(
            CartService.objects.filter(cart=self.cart).count(),
            0,
        )

        self.cart.refresh_from_db()

        self.assertIsNone(self.cart.accommodation)
        self.assertIsNone(self.cart.nights)
        self.assertIsNone(self.cart.price_total)


class RemoveFromCartViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        self.accommodation_type = AccommodationType.objects.create(name="Hotel")

        self.accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
        )

        self.cart = Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
            nights=2,
            price_total=100000,
        )

        self.client.force_login(self.user)

    def test_remove_accommodation_from_cart(self):
        response = self.client.post(reverse("remove_from_cart"))

        self.assertRedirects(response, reverse("cart"))

        self.cart.refresh_from_db()

        self.assertIsNone(self.cart.accommodation)
        self.assertIsNone(self.cart.nights)
        self.assertIsNone(self.cart.price_total)


class RemoveActivityViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        activity_type = ActivityType.objects.create(name="Tour")

        activity = Activity.objects.create(
            host=self.user,
            activity_type=activity_type,
            name="Tour",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        self.cart = Cart.objects.create(user=self.user)

        self.cart_activity = CartActivity.objects.create(
            cart=self.cart,
            activity=activity,
            total_price=Decimal("20000.00"),
            date=date(2026, 10, 1),
        )

        self.client.force_login(self.user)

    def test_remove_activity_from_cart(self):
        response = self.client.post(
            reverse(
                "remove_activity",
                kwargs={"pk": self.cart_activity.pk},
            )
        )

        self.assertRedirects(response, reverse("cart"))
        self.assertFalse(CartActivity.objects.filter(pk=self.cart_activity.pk).exists())


class RemoveServiceViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        service_type = ServiceType.objects.create(name="Transporte")

        service = Service.objects.create(
            host=self.user,
            service_type=service_type,
            name="Transporte",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        self.cart = Cart.objects.create(user=self.user)

        self.cart_service = CartService.objects.create(
            cart=self.cart,
            service=service,
            total_price=Decimal("15000.00"),
            date=date(2026, 10, 1),
        )

        self.client.force_login(self.user)

    def test_remove_service_from_cart(self):
        response = self.client.post(
            reverse(
                "remove_service",
                kwargs={"pk": self.cart_service.pk},
            )
        )

        self.assertRedirects(response, reverse("cart"))
        self.assertFalse(CartService.objects.filter(pk=self.cart_service.pk).exists())


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        self.client.force_login(self.user)

    def test_anonymous_user_cannot_checkout(self):
        self.client.logout()

        response = self.client.post(
            reverse("checkout"),
            {},
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_checkout_rejects_missing_card_number(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertIn("número de tarjeta inválido", unquote(response.url))

    def test_checkout_rejects_invalid_card_length(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "411111111111",
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertIn("número de tarjeta inválido", unquote(response.url))

    def test_checkout_rejects_invalid_luhn_card(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "4111111111111112",
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertIn("tarjeta no válida", unquote(response.url))

    def test_checkout_rejects_expired_card(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "4111111111111111",
                "expiry": "01/20",
                "cvv": "123",
            },
        )

        self.assertIn("tarjeta vencida", unquote(response.url))

    def test_checkout_rejects_invalid_cvv(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "4111111111111111",
                "expiry": "12/99",
                "cvv": "000",
            },
        )

        self.assertIn("CVV inválido", unquote(response.url))

    def test_checkout_rejects_non_visa_card(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "5111111111111118",
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertIn("solo se aceptan tarjetas Visa", unquote(response.url))

    def test_checkout_without_cart_still_redirects_successfully(self):
        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "4111111111111111",
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Pago realizado con éxito", unquote(response.url))

    def test_checkout_creates_reservation_invoice_and_items(self):
        accommodation_type = AccommodationType.objects.create(name="Hotel")

        accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=accommodation_type,
            name="Hotel Test",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
        )

        activity_type = ActivityType.objects.create(name="Tour")
        service_type = ServiceType.objects.create(name="Servicio")

        activity = Activity.objects.create(
            host=self.user,
            activity_type=activity_type,
            name="Tour",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        service = Service.objects.create(
            host=self.user,
            service_type=service_type,
            name="Servicio",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        cart = Cart.objects.create(
            user=self.user,
            accommodation=accommodation,
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 5),
            nights=4,
            price_total=200000,
        )

        CartActivity.objects.create(
            cart=cart,
            activity=activity,
            total_price=Decimal("20000.00"),
            date=date(2026, 10, 2),
        )

        CartService.objects.create(
            cart=cart,
            service=service,
            total_price=Decimal("15000.00"),
            date=date(2026, 10, 3),
        )

        response = self.client.post(
            reverse("checkout"),
            {
                "card_number": "4111111111111111",
                "expiry": "12/99",
                "cvv": "123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("Pago realizado con éxito", unquote(response.url))

        reservation = Reservation.objects.get(guest=self.user)

        self.assertEqual(
            reservation.accommodation,
            accommodation,
        )
        self.assertEqual(reservation.status, "CONFIRMED")

        invoice = Invoice.objects.get(reservation=reservation)

        self.assertEqual(
            invoice.amount,
            Decimal("235000.00"),
        )
        self.assertTrue(invoice.payment_method.startswith("Card-"))

        self.assertEqual(
            InvoiceItem.objects.filter(invoice=invoice).count(),
            3,
        )

        self.assertEqual(
            ReservationActivity.objects.filter(reservation=reservation).count(),
            1,
        )

        self.assertEqual(
            ReservationService.objects.filter(reservation=reservation).count(),
            1,
        )

        self.assertEqual(
            CartActivity.objects.filter(cart=cart).count(),
            0,
        )

        self.assertEqual(
            CartService.objects.filter(cart=cart).count(),
            0,
        )

        cart.refresh_from_db()

        self.assertIsNone(cart.accommodation)
        self.assertIsNone(cart.start_date)
        self.assertIsNone(cart.end_date)
        self.assertIsNone(cart.nights)
        self.assertIsNone(cart.price_total)
