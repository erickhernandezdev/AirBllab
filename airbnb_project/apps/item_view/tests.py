from datetime import date

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
    Reservation,
    ReservationActivity,
    ReservationService,
    Service,
    ServiceType,
)


class ItemViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            name="Test User",
        )

        self.other_user = CustomUser.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="TestPassword123!",
            name="Other User",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel",
            description="Hotel test",
        )

        self.activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour test",
        )

        self.service_type = ServiceType.objects.create(
            name="Spa",
            description="Spa test",
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

        self.service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Test Spa",
            description="Servicio de prueba",
            price=15000,
            rating=4.5,
            status="Aprobado",
        )

    def test_invalid_type_returns_404(self):
        response = self.client.get(
            reverse("detail", kwargs={"tipo": "invalid", "id": 1})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_accommodation_detail(self):
        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "accomodations",
                    "id": self.accommodation.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "item_view.html")
        self.assertEqual(response.context["item"], self.accommodation)
        self.assertEqual(response.context["tipo"], "accomodations")
        self.assertEqual(response.context["blocked_dates"], [])
        self.assertFalse(response.context["already_in_cart"])

    def test_service_detail(self):
        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "services",
                    "id": self.service.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["item"], self.service)
        self.assertEqual(response.context["tipo"], "services")

    def test_activity_detail(self):
        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "experiences",
                    "id": self.activity.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["item"], self.activity)
        self.assertEqual(response.context["tipo"], "experiences")

    def test_nonexistent_item_returns_404(self):
        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "accomodations",
                    "id": 9999,
                },
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_accommodation_blocked_dates_include_entire_reservation_range(self):
        Reservation.objects.create(
            guest=self.other_user,
            accommodation=self.accommodation,
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 22),
            status="CONFIRMED",
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "accomodations",
                    "id": self.accommodation.id,
                },
            )
        )

        self.assertEqual(
            response.context["blocked_dates"],
            ["2026-09-20", "2026-09-21", "2026-09-22"],
        )

    def test_service_blocked_dates(self):
        reservation = Reservation.objects.create(
            guest=self.other_user,
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 22),
            status="CONFIRMED",
        )

        ReservationService.objects.create(
            reservation=reservation,
            service=self.service,
            total_price=15000,
            date=date(2026, 9, 21),
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "services",
                    "id": self.service.id,
                },
            )
        )

        self.assertEqual(
            response.context["blocked_dates"],
            ["2026-09-21"],
        )

    def test_activity_blocked_dates(self):
        reservation = Reservation.objects.create(
            guest=self.other_user,
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 22),
            status="CONFIRMED",
        )

        ReservationActivity.objects.create(
            reservation=reservation,
            activity=self.activity,
            total_price=20000,
            date=date(2026, 9, 22),
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "experiences",
                    "id": self.activity.id,
                },
            )
        )

        self.assertEqual(
            response.context["blocked_dates"],
            ["2026-09-22"],
        )

    def test_authenticated_user_detects_accommodation_in_cart(self):
        self.client.force_login(self.user)

        Cart.objects.create(
            user=self.user,
            accommodation=self.accommodation,
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "accomodations",
                    "id": self.accommodation.id,
                },
            )
        )

        self.assertTrue(response.context["already_in_cart"])

    def test_authenticated_user_detects_service_in_cart(self):
        self.client.force_login(self.user)

        cart = Cart.objects.create(user=self.user)

        CartService.objects.create(
            cart=cart,
            service=self.service,
            total_price=15000,
            date=date(2026, 9, 25),
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "services",
                    "id": self.service.id,
                },
            )
        )

        self.assertTrue(response.context["already_in_cart"])

    def test_authenticated_user_detects_activity_in_cart(self):
        self.client.force_login(self.user)

        cart = Cart.objects.create(user=self.user)

        CartActivity.objects.create(
            cart=cart,
            activity=self.activity,
            total_price=20000,
            date=date(2026, 9, 25),
        )

        response = self.client.get(
            reverse(
                "detail",
                kwargs={
                    "tipo": "experiences",
                    "id": self.activity.id,
                },
            )
        )

        self.assertTrue(response.context["already_in_cart"])
