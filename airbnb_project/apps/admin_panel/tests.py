from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.admin_panel.models import ApprovalLog
from apps.core.models import (
    Accommodation,
    AccommodationType,
    Activity,
    ActivityType,
    CustomUser,
    Service,
    ServiceType,
)

User = get_user_model()


class AdminPanelTestBase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="TestPassword123!",
            name="Admin User",
            role="ADMIN",
        )

        self.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="TestPassword123!",
            name="Regular User",
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

        self.accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Test Hotel",
            description="Hotel de prueba",
            location="San José",
            price=50000,
            rating=4.5,
            status="Pendiente",
        )

        self.activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Test Tour",
            description="Tour de prueba",
            location="Cartago",
            price=20000,
            rating=4.5,
            status="Pendiente",
        )

        self.service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Test Spa",
            description="Servicio de prueba",
            price=15000,
            rating=4.5,
            status="Pendiente",
        )


class AdminAccessTest(AdminPanelTestBase):
    def test_anonymous_user_is_redirected(self):
        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        self.assertRedirects(
            response,
            reverse("homepage"),
            fetch_redirect_response=False,
        )

    def test_regular_user_is_redirected(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        self.assertRedirects(
            response,
            reverse("homepage"),
            fetch_redirect_response=False,
        )

    def test_regular_user_cannot_access_pending_approval(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin_panel:admin_pending_approval"))

        self.assertRedirects(
            response,
            reverse("homepage"),
            fetch_redirect_response=False,
        )

    def test_regular_user_cannot_access_user_list(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin_panel:admin_user_list"))

        self.assertRedirects(
            response,
            reverse("homepage"),
            fetch_redirect_response=False,
        )


class AdminDashboardTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_dashboard_is_accessible(self):
        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/dashboard.html",
        )

    def test_dashboard_contains_statistics(self):
        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        stats = response.context["stats"]

        self.assertEqual(stats["total_users"], 2)
        self.assertEqual(stats["total_accommodations"], 1)
        self.assertEqual(stats["total_activities"], 1)
        self.assertEqual(stats["total_services"], 1)

    def test_dashboard_counts_pending_items(self):
        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        stats = response.context["stats"]

        self.assertEqual(stats["pending_accommodations"], 1)
        self.assertEqual(stats["pending_activities"], 1)
        self.assertEqual(stats["pending_services"], 1)

    def test_dashboard_contains_recent_approvals(self):
        ApprovalLog.objects.create(
            admin_user=self.admin,
            accommodation=self.accommodation,
            status="approved",
            notes="Approved test",
        )

        response = self.client.get(reverse("admin_panel:admin_dashboard"))

        recent = response.context["stats"]["recent_approvals"]

        self.assertEqual(recent.count(), 1)


class PendingApprovalListTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_pending_approval_page_is_accessible(self):
        response = self.client.get(reverse("admin_panel:admin_pending_approval"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/pending_approval.html",
        )

    def test_pending_approval_contains_pending_items(self):
        response = self.client.get(reverse("admin_panel:admin_pending_approval"))

        self.assertEqual(
            list(response.context["pending_accommodations"]),
            [self.accommodation],
        )

        self.assertEqual(
            list(response.context["pending_activities"]),
            [self.activity],
        )

        self.assertEqual(
            list(response.context["pending_services"]),
            [self.service],
        )

    def test_approved_items_are_not_in_pending_list(self):
        self.accommodation.status = "Aprobado"
        self.accommodation.save()

        response = self.client.get(reverse("admin_panel:admin_pending_approval"))

        self.assertNotIn(
            self.accommodation,
            response.context["pending_accommodations"],
        )


class ApprovalDetailTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_accommodation_approval_detail(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_approval_detail",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/approval_accommodation_detail.html",
        )
        self.assertEqual(
            response.context["item"],
            self.accommodation,
        )
        self.assertEqual(
            response.context["item_type"],
            "accommodation",
        )

    def test_activity_approval_detail(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_approval_detail",
                kwargs={
                    "item_type": "activity",
                    "item_id": self.activity.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/approval_activity_detail.html",
        )
        self.assertEqual(response.context["item"], self.activity)

    def test_service_approval_detail(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_approval_detail",
                kwargs={
                    "item_type": "service",
                    "item_id": self.service.id,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/approval_service_detail.html",
        )
        self.assertEqual(response.context["item"], self.service)

    def test_invalid_item_type_redirects(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_approval_detail",
                kwargs={
                    "item_type": "invalid",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

    def test_approval_detail_contains_logs(self):
        log = ApprovalLog.objects.create(
            admin_user=self.admin,
            accommodation=self.accommodation,
            status="approved",
            notes="Approved",
        )

        response = self.client.get(
            reverse(
                "admin_panel:admin_approval_detail",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertEqual(
            list(response.context["approval_logs"]),
            [log],
        )


class ApproveItemTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_approve_accommodation(self):
        response = self.client.post(
            reverse(
                "admin_panel:admin_approve_item",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            ),
            {"notes": "Everything is correct"},
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

        self.accommodation.refresh_from_db()

        self.assertEqual(
            self.accommodation.status,
            "Aprobado",
        )

        self.assertTrue(
            ApprovalLog.objects.filter(
                accommodation=self.accommodation,
                admin_user=self.admin,
                status="approved",
                notes="Everything is correct",
            ).exists()
        )

    def test_approve_activity(self):
        self.client.post(
            reverse(
                "admin_panel:admin_approve_item",
                kwargs={
                    "item_type": "activity",
                    "item_id": self.activity.id,
                },
            )
        )

        self.activity.refresh_from_db()

        self.assertEqual(self.activity.status, "Aprobado")

        self.assertTrue(
            ApprovalLog.objects.filter(
                activity=self.activity,
                status="approved",
            ).exists()
        )

    def test_approve_service(self):
        self.client.post(
            reverse(
                "admin_panel:admin_approve_item",
                kwargs={
                    "item_type": "service",
                    "item_id": self.service.id,
                },
            )
        )

        self.service.refresh_from_db()

        self.assertEqual(self.service.status, "Aprobado")

        self.assertTrue(
            ApprovalLog.objects.filter(
                service=self.service,
                status="approved",
            ).exists()
        )

    def test_invalid_approval_type_redirects(self):
        response = self.client.post(
            reverse(
                "admin_panel:admin_approve_item",
                kwargs={
                    "item_type": "invalid",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

    def test_approve_get_request_redirects_without_changes(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_approve_item",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

        self.accommodation.refresh_from_db()

        self.assertEqual(
            self.accommodation.status,
            "Pendiente",
        )


class RejectItemTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_reject_accommodation(self):
        response = self.client.post(
            reverse(
                "admin_panel:admin_reject_item",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            ),
            {"notes": "Information is incomplete"},
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

        self.accommodation.refresh_from_db()

        self.assertEqual(
            self.accommodation.status,
            "Rechazado",
        )

        self.assertTrue(
            ApprovalLog.objects.filter(
                accommodation=self.accommodation,
                admin_user=self.admin,
                status="rejected",
                notes="Information is incomplete",
            ).exists()
        )

    def test_reject_activity(self):
        self.client.post(
            reverse(
                "admin_panel:admin_reject_item",
                kwargs={
                    "item_type": "activity",
                    "item_id": self.activity.id,
                },
            ),
            {"notes": "Invalid activity"},
        )

        self.activity.refresh_from_db()

        self.assertEqual(
            self.activity.status,
            "Rechazado",
        )

        self.assertTrue(
            ApprovalLog.objects.filter(
                activity=self.activity,
                status="rejected",
            ).exists()
        )

    def test_reject_service(self):
        self.client.post(
            reverse(
                "admin_panel:admin_reject_item",
                kwargs={
                    "item_type": "service",
                    "item_id": self.service.id,
                },
            )
        )

        self.service.refresh_from_db()

        self.assertEqual(
            self.service.status,
            "Rechazado",
        )

        self.assertTrue(
            ApprovalLog.objects.filter(
                service=self.service,
                status="rejected",
                notes="Razón no especificada",
            ).exists()
        )

    def test_invalid_rejection_type_redirects(self):
        response = self.client.post(
            reverse(
                "admin_panel:admin_reject_item",
                kwargs={
                    "item_type": "invalid",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

    def test_reject_get_request_redirects_without_changes(self):
        response = self.client.get(
            reverse(
                "admin_panel:admin_reject_item",
                kwargs={
                    "item_type": "accommodation",
                    "item_id": self.accommodation.id,
                },
            )
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_pending_approval"),
            fetch_redirect_response=False,
        )

        self.accommodation.refresh_from_db()

        self.assertEqual(
            self.accommodation.status,
            "Pendiente",
        )


class UserListTest(AdminPanelTestBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)

    def test_user_list_is_accessible(self):
        response = self.client.get(reverse("admin_panel:admin_user_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "admin_panel/user_list.html",
        )

    def test_user_list_contains_users(self):
        response = self.client.get(reverse("admin_panel:admin_user_list"))

        users = response.context["users"]

        self.assertIn(self.admin, users)
        self.assertIn(self.user, users)

    def test_user_statistics_are_correct(self):
        response = self.client.get(reverse("admin_panel:admin_user_list"))

        stats = response.context["user_stats"]

        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["admins"], 1)
        self.assertEqual(stats["regular_users"], 1)

    def test_user_list_is_ordered_by_creation_date(self):
        response = self.client.get(reverse("admin_panel:admin_user_list"))

        users = list(response.context["users"])

        self.assertEqual(users[0], self.user)
        self.assertEqual(users[1], self.admin)


class ApprovalLogPropertiesTest(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="TestPassword123!",
            name="Admin",
            role="ADMIN",
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

        self.accommodation = Accommodation.objects.create(
            host=self.admin,
            accommodation_type=self.accommodation_type,
            name="Test Hotel",
            description="Hotel de prueba",
            location="San José",
            price=50000,
            status="Pendiente",
        )

        self.service = Service.objects.create(
            host=self.admin,
            service_type=self.service_type,
            name="Test Spa",
            description="Spa de prueba",
            price=15000,
            status="Pendiente",
        )

        self.activity = Activity.objects.create(
            host=self.admin,
            activity_type=self.activity_type,
            name="Test Tour",
            description="Tour de prueba",
            location="Cartago",
            price=20000,
            status="Pendiente",
        )

    def test_accommodation_properties(self):
        log = ApprovalLog.objects.create(
            admin_user=self.admin,
            accommodation=self.accommodation,
            status="approved",
        )

        self.assertEqual(
            str(log),
            "Alojamiento: Test Hotel - Aprobado",
        )
        self.assertEqual(log.item_name, "Test Hotel")
        self.assertEqual(log.item_type, "accommodation")

    def test_activity_properties(self):
        log = ApprovalLog.objects.create(
            admin_user=self.admin,
            activity=self.activity,
            status="approved",
        )

        self.assertEqual(
            str(log),
            "Actividad: Test Tour - Aprobado",
        )
        self.assertEqual(log.item_name, "Test Tour")
        self.assertEqual(log.item_type, "activity")

    def test_service_properties(self):
        log = ApprovalLog.objects.create(
            admin_user=self.admin,
            service=self.service,
            status="approved",
        )

        self.assertEqual(
            str(log),
            "Servicio: Test Spa - Aprobado",
        )
        self.assertEqual(log.item_name, "Test Spa")
        self.assertEqual(log.item_type, "service")

    def test_properties_without_item(self):
        log = ApprovalLog.objects.create(
            admin_user=self.admin,
            status="approved",
        )

        self.assertEqual(
            str(log),
            f"Aprobación #{log.id}",
        )
        self.assertEqual(log.item_name, "N/A")
        self.assertEqual(log.item_type, "unknown")
