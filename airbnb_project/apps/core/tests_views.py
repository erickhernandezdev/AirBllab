from django.test import TestCase
from django.urls import reverse

from apps.core.models import (
    AccommodationType,
    ActivityType,
    ServiceType,
)


class GetSubtypesViewTest(TestCase):
    def setUp(self):
        self.url = reverse("get_subtypes")

        AccommodationType.objects.create(
            name="Hotel",
            description="Hotel de prueba",
        )
        AccommodationType.objects.create(
            name="Casa",
            description="Casa de prueba",
        )

        ServiceType.objects.create(
            name="Spa",
            description="Spa de prueba",
        )

        ActivityType.objects.create(
            name="Tour",
            description="Tour de prueba",
        )

    def test_returns_accommodation_subtypes(self):
        response = self.client.get(
            self.url,
            {"type": "Alojamiento"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"subtypes": ["Hotel", "Casa"]},
        )

    def test_returns_service_subtypes(self):
        response = self.client.get(
            self.url,
            {"type": "Servicio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"subtypes": ["Spa"]},
        )

    def test_returns_activity_subtypes(self):
        response = self.client.get(
            self.url,
            {"type": "Actividad"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"subtypes": ["Tour"]},
        )

    def test_invalid_type_returns_empty_list(self):
        response = self.client.get(
            self.url,
            {"type": "Invalid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"subtypes": []},
        )

    def test_missing_type_returns_empty_list(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"subtypes": []},
        )
