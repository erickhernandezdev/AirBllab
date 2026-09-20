from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from apps.core.models import CustomUser


class LoginViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        self.admin = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            name="Admin User",
            role=CustomUser.Role.ADMIN,
        )

    @patch("apps.login.views.set_user_context")
    def test_login_success_redirects_to_homepage(self, mock_set_context):
        response = self.client.post(
            reverse("login"),
            {
                "email": "test@example.com",
                "password": "password123",
            },
        )

        self.assertRedirects(response, reverse("homepage"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        mock_set_context.assert_called_once_with(self.user)

    @patch("apps.login.views.set_user_context")
    def test_admin_login_redirects_to_admin_dashboard(self, mock_set_context):
        response = self.client.post(
            reverse("login"),
            {
                "email": "admin@example.com",
                "password": "password123",
            },
        )

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_dashboard"),
        )
        mock_set_context.assert_called_once_with(self.admin)

    def test_invalid_login_renders_form(self):
        response = self.client.post(
            reverse("login"),
            {
                "email": "test@example.com",
                "password": "wrongpassword",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, "login/login.html")

    def test_get_login_page(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login/login.html")

    @patch("apps.login.views.set_user_context")
    def test_login_redirects_to_next_url(self, mock_set_context):
        response = self.client.post(
            reverse("login") + "?next=/cart/",
            {
                "email": "test@example.com",
                "password": "password123",
                "next": "/cart/",
            },
        )

        self.assertRedirects(response, "/cart/")
        mock_set_context.assert_called_once_with(self.user)

    def test_authenticated_user_redirects_to_homepage(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("login"))

        self.assertRedirects(response, reverse("homepage"))

    def test_authenticated_admin_redirects_to_dashboard(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("login"))

        self.assertRedirects(
            response,
            reverse("admin_panel:admin_dashboard"),
        )


class LogoutViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

    def test_logout_redirects_to_homepage(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("homepage"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
