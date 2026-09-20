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


class MyPublicationsViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
            name="Test User",
            role="USER",
        )

        self.other_user = CustomUser.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="TestPassword123!",
            name="Other User",
            role="USER",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel",
            description="Hotel de prueba",
        )

        self.service_type = ServiceType.objects.create(
            name="Spa",
            description="Spa de prueba",
        )

        self.activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour de prueba",
        )

        self.url = reverse("my_publications")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_authenticated_user_can_access_publications(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "my_publications/my_publications.html",
        )

    def test_only_current_user_publications_are_returned(self):
        self.client.force_login(self.user)

        accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="My Hotel",
            description="My accommodation",
            location="San José",
            price=50000,
            status="Aprobado",
        )

        service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="My Spa",
            description="My service",
            price=15000,
            status="Pendiente",
        )

        activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="My Tour",
            description="My activity",
            location="Cartago",
            price=20000,
            status="Aprobado",
        )

        Accommodation.objects.create(
            host=self.other_user,
            accommodation_type=self.accommodation_type,
            name="Other Hotel",
            description="Other accommodation",
            location="Alajuela",
            price=60000,
            status="Aprobado",
        )

        response = self.client.get(self.url)

        publications = response.context["publications"]

        self.assertEqual(len(publications), 3)
        self.assertIn(accommodation, publications)
        self.assertIn(service, publications)
        self.assertIn(activity, publications)

        self.assertNotContains(response, "Other Hotel")

    def test_user_with_no_publications_gets_empty_list(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["publications"], [])
