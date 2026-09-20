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

from .views import build_card


class BuildCardTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host",
        )

        self.accommodation_type = AccommodationType.objects.create(name="Hotel")

    def test_build_card_creates_correct_data(self):
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

        card = build_card(accommodation, "accomodations")

        self.assertEqual(card["alt"], "Hotel Test")
        self.assertEqual(card["title"], "Hotel Test")
        self.assertEqual(card["price"], "₡50,000.00 por noche")
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

    def test_build_card_uses_default_image_when_no_image(self):
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

        card = build_card(accommodation, "accomodations")

        self.assertEqual(
            card["image"],
            "../../media/default.png",
        )


class ListingsViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host",
        )

        self.accommodation_type = AccommodationType.objects.create(name="Hotel")

        self.activity_type = ActivityType.objects.create(name="Tour")

        self.service_type = ServiceType.objects.create(name="Transporte")

    def test_accommodations_listing(self):
        Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Hotel",
            location="San José",
            price=Decimal("50000.00"),
            rating=4.5,
            status="Aprobado",
        )

        response = self.client.get(reverse("listing", kwargs={"tipo": "accomodations"}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "listings.html")
        self.assertEqual(
            response.context["title"],
            "Tu próximo destino te espera",
        )
        self.assertEqual(len(response.context["items"]), 1)

    def test_experiences_listing(self):
        Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Tour Test",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
            rating=4.8,
            status="Aprobado",
        )

        response = self.client.get(reverse("listing", kwargs={"tipo": "experiences"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["title"],
            "Vive momentos que dejan huella",
        )
        self.assertEqual(len(response.context["items"]), 1)

    def test_services_listing(self):
        Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Transporte Test",
            description="Servicio",
            price=Decimal("15000.00"),
            rating=4.7,
            status="Aprobado",
        )

        response = self.client.get(reverse("listing", kwargs={"tipo": "services"}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["title"],
            "Cuida tu cuerpo, tu tiempo y tu espacio",
        )
        self.assertEqual(len(response.context["items"]), 1)

    def test_listing_only_shows_approved_items(self):
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

        response = self.client.get(reverse("listing", kwargs={"tipo": "accomodations"}))

        items = response.context["items"]

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Hotel Aprobado")

    def test_listing_creates_four_sections(self):
        response = self.client.get(reverse("listing", kwargs={"tipo": "accomodations"}))

        sections = response.context["sections"]

        self.assertEqual(len(sections), 4)
        self.assertEqual(sections[0]["title"], "Cerca de ti")
        self.assertEqual(
            sections[1]["title"],
            "Disponibles el próximo fin de semana",
        )
        self.assertEqual(
            sections[2]["title"],
            "Te podrían gustar",
        )
        self.assertEqual(
            sections[3]["title"],
            "Mejor valorados",
        )

    def test_invalid_listing_type_returns_404(self):
        response = self.client.get(reverse("listing", kwargs={"tipo": "invalid"}))

        self.assertEqual(response.status_code, 404)

    def test_listing_limits_results_to_five_items(self):
        for i in range(7):
            Accommodation.objects.create(
                host=self.user,
                accommodation_type=self.accommodation_type,
                name=f"Hotel {i}",
                description="Hotel",
                location="San José",
                price=Decimal("50000.00"),
                status="Aprobado",
            )

        response = self.client.get(reverse("listing", kwargs={"tipo": "accomodations"}))

        self.assertEqual(len(response.context["items"]), 5)
