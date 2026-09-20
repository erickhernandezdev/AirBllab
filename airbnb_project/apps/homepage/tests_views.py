from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.core.models import (
    Accommodation,
    AccommodationType,
    Activity,
    ActivityType,
    CustomUser,
    Service,
    ServiceType,
)


class HomepageViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host User",
        )

        self.accommodation_type = AccommodationType.objects.create(name="Hotel")

        self.activity_type = ActivityType.objects.create(name="Tour")

        self.service_type = ServiceType.objects.create(name="Transporte")

    def test_homepage_returns_200(self):
        response = self.client.get(reverse("homepage"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_contains_main_cards(self):
        response = self.client.get(reverse("homepage"))

        cards = response.context["cards"]

        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0]["alt"], "Alojamiento")
        self.assertEqual(cards[1]["alt"], "Experiencia")
        self.assertEqual(cards[2]["alt"], "Servicios")

    def test_homepage_only_shows_approved_items(self):
        Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Aprobado",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
            status="Aprobado",
        )

        Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Pendiente",
            description="Hotel",
            location="Alajuela",
            price=Decimal("40000.00"),
            status="Pendiente",
        )

        response = self.client.get(reverse("homepage"))

        accommodations = response.context["accommodations"]

        self.assertEqual(len(accommodations), 1)
        self.assertEqual(
            accommodations[0]["title"],
            "Hotel Aprobado",
        )

    def test_homepage_builds_accommodation_card(self):
        accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
            rating=4.5,
            status="Aprobado",
        )

        response = self.client.get(reverse("homepage"))

        card = response.context["accommodations"][0]

        self.assertEqual(card["alt"], accommodation.name)
        self.assertEqual(card["title"], accommodation.name)
        self.assertEqual(card["price"], "₡50,000.00")
        self.assertEqual(card["rating"], "4.5")
        self.assertEqual(
            card["link"],
            reverse(
                "detail",
                kwargs={
                    "tipo": "accomodations",
                    "id": accommodation.id,
                },
            ),
        )

    def test_homepage_builds_activity_card(self):
        activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Tour Test",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
            rating=4.8,
            status="Aprobado",
        )

        response = self.client.get(reverse("homepage"))

        card = response.context["experiences"][0]

        self.assertEqual(card["title"], activity.name)
        self.assertEqual(card["price"], "₡20,000.00")
        self.assertEqual(card["rating"], "4.8")
        self.assertEqual(
            card["link"],
            reverse(
                "detail",
                kwargs={
                    "tipo": "experiences",
                    "id": activity.id,
                },
            ),
        )

    def test_homepage_builds_service_card(self):
        service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Transporte Test",
            description="Servicio",
            price=Decimal("15000.00"),
            rating=4.7,
            status="Aprobado",
        )

        response = self.client.get(reverse("homepage"))

        card = response.context["services"][0]

        self.assertEqual(card["title"], service.name)
        self.assertEqual(card["price"], "₡15,000.00")
        self.assertEqual(card["rating"], "4.7")
        self.assertEqual(
            card["link"],
            reverse(
                "detail",
                kwargs={
                    "tipo": "services",
                    "id": service.id,
                },
            ),
        )
