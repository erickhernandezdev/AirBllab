from datetime import date

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


class NewProposalTestBase(TestCase):
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

        self.activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour test",
        )

        self.service_type = ServiceType.objects.create(
            name="Spa",
            description="Spa test",
        )

        self.url = reverse("new_proposal")


class NewProposalAccessTest(NewProposalTestBase):
    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_authenticated_user_can_access_page(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "new_proposal/new_proposal.html",
        )

    def test_get_request_contains_empty_form(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertIn("form", response.context)
        self.assertFalse(response.context["form"].is_bound)


class NewProposalFormTest(NewProposalTestBase):
    def test_accommodation_subtypes_are_loaded(self):
        from .forms import NewProposalForm

        form = NewProposalForm(selected_type="Alojamiento")

        self.assertIn(
            ("Hotel", "Hotel"),
            form.fields["subtype"].choices,
        )

    def test_activity_subtypes_are_loaded(self):
        from .forms import NewProposalForm

        form = NewProposalForm(selected_type="Actividad")

        self.assertIn(
            ("Tour", "Tour"),
            form.fields["subtype"].choices,
        )

    def test_service_subtypes_are_loaded(self):
        from .forms import NewProposalForm

        form = NewProposalForm(selected_type="Servicio")

        self.assertIn(
            ("Spa", "Spa"),
            form.fields["subtype"].choices,
        )

    def test_no_subtypes_are_loaded_without_type(self):
        from .forms import NewProposalForm

        form = NewProposalForm()

        self.assertEqual(
            list(form.fields["subtype"].choices),
            [],
        )

    def test_end_date_cannot_be_before_start_date(self):
        from .forms import NewProposalForm

        form = NewProposalForm(
            data={
                "name": "Test",
                "description": "Description",
                "type": "Alojamiento",
                "subtype": "Hotel",
                "location": "San José",
                "start_date": "2026-10-20",
                "end_date": "2026-10-10",
                "price": "50000.00",
            },
            selected_type="Alojamiento",
        )

        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_end_date_can_equal_start_date(self):
        from .forms import NewProposalForm

        form = NewProposalForm(
            data={
                "name": "Test",
                "description": "Description",
                "type": "Alojamiento",
                "subtype": "Hotel",
                "location": "San José",
                "start_date": "2026-10-20",
                "end_date": "2026-10-20",
                "price": "50000.00",
            },
            selected_type="Alojamiento",
        )

        self.assertTrue(form.is_valid())


class NewProposalCreationTest(NewProposalTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

        self.base_data = {
            "name": "Nueva propuesta",
            "description": "Descripción de prueba",
            "location": "San José",
            "start_date": "2026-10-20",
            "end_date": "2026-10-25",
            "price": "50000.00",
        }

    def test_create_accommodation(self):
        data = {
            **self.base_data,
            "type": "Alojamiento",
            "subtype": "Hotel",
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,
            reverse("my_publications"),
            fetch_redirect_response=False,
        )

        accommodation = Accommodation.objects.get(name="Nueva propuesta")

        self.assertEqual(accommodation.host, self.user)
        self.assertEqual(
            accommodation.accommodation_type,
            self.accommodation_type,
        )
        self.assertEqual(
            accommodation.description,
            "Descripción de prueba",
        )
        self.assertEqual(
            accommodation.location,
            "San José",
        )
        self.assertEqual(
            accommodation.price,
            50000,
        )
        self.assertEqual(
            accommodation.available_from,
            date(2026, 10, 20),
        )
        self.assertEqual(
            accommodation.available_to,
            date(2026, 10, 25),
        )
        self.assertEqual(
            accommodation.status,
            "Pendiente",
        )

    def test_create_activity(self):
        data = {
            **self.base_data,
            "type": "Actividad",
            "subtype": "Tour",
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,
            reverse("my_publications"),
            fetch_redirect_response=False,
        )

        activity = Activity.objects.get(name="Nueva propuesta")

        self.assertEqual(activity.host, self.user)
        self.assertEqual(
            activity.activity_type,
            self.activity_type,
        )
        self.assertEqual(activity.description, "Descripción de prueba")
        self.assertEqual(activity.location, "San José")
        self.assertEqual(activity.price, 50000)
        self.assertEqual(activity.status, "Pendiente")

    def test_create_service(self):
        data = {
            **self.base_data,
            "type": "Servicio",
            "subtype": "Spa",
        }

        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,
            reverse("my_publications"),
            fetch_redirect_response=False,
        )

        service = Service.objects.get(name="Nueva propuesta")

        self.assertEqual(service.host, self.user)
        self.assertEqual(
            service.service_type,
            self.service_type,
        )
        self.assertEqual(service.description, "Descripción de prueba")
        self.assertEqual(service.price, 50000)
        self.assertEqual(service.status, "Pendiente")

    def test_invalid_form_does_not_create_proposal(self):
        data = {
            "name": "",
            "description": "",
            "type": "Alojamiento",
            "subtype": "Hotel",
            "location": "",
            "start_date": "2026-10-20",
            "end_date": "2026-10-25",
            "price": "50000.00",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "new_proposal/new_proposal.html",
        )

        self.assertEqual(
            Accommodation.objects.count(),
            0,
        )

    def test_accommodation_requires_matching_subtype(self):
        data = {
            **self.base_data,
            "type": "Alojamiento",
            "subtype": "DoesNotExist",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Accommodation.objects.count(),
            0,
        )

    def test_created_proposal_is_pending(self):
        data = {
            **self.base_data,
            "type": "Servicio",
            "subtype": "Spa",
        }

        self.client.post(self.url, data)

        service = Service.objects.get(name="Nueva propuesta")

        self.assertEqual(service.status, "Pendiente")

    def test_optional_image_is_allowed(self):
        data = {
            **self.base_data,
            "type": "Actividad",
            "subtype": "Tour",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Activity.objects.filter(name="Nueva propuesta").exists())
