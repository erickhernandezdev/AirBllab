from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.core.models import CustomUser, Invoice, Reservation


class HistoryViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="Test User",
        )

        self.other_user = CustomUser.objects.create_user(
            username="other",
            email="other@example.com",
            password="password123",
            name="Other User",
        )

        self.reservation = Reservation.objects.create(
            guest=self.user,
            status="Pendiente",
        )

        self.other_reservation = Reservation.objects.create(
            guest=self.other_user,
            status="Pendiente",
        )

    def test_authenticated_user_can_access_history(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("history"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "history.html")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("history"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/account/login/", response.url)

    def test_history_only_contains_user_invoices(self):
        user_invoice = Invoice.objects.create(
            reservation=self.reservation,
            amount=Decimal("50000.00"),
            payment_method="Tarjeta",
            paid_at="2026-10-01T12:00:00Z",
        )

        other_invoice = Invoice.objects.create(
            reservation=self.other_reservation,
            amount=Decimal("30000.00"),
            payment_method="Tarjeta",
            paid_at="2026-10-02T12:00:00Z",
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse("history"))

        invoices = response.context["invoices"]

        self.assertEqual(invoices.count(), 1)
        self.assertEqual(invoices.first(), user_invoice)
        self.assertNotIn(other_invoice, invoices)

    def test_history_is_empty_when_user_has_no_invoices(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("history"))

        invoices = response.context["invoices"]

        self.assertEqual(invoices.count(), 0)
