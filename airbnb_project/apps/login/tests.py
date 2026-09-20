from django.test import RequestFactory, TestCase

from apps.core.models import CustomUser

from .forms import LoginForm


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        self.request = RequestFactory().post("/account/login/")

    def test_valid_credentials(self):
        form = LoginForm(
            data={
                "email": "test@example.com",
                "password": "password123",
            },
            request=self.request,
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["user"], self.user)

    def test_invalid_password(self):
        form = LoginForm(
            data={
                "email": "test@example.com",
                "password": "wrongpassword",
            },
            request=self.request,
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Correo o contraseña incorrectos.",
            form.non_field_errors(),
        )

    def test_nonexistent_user(self):
        form = LoginForm(
            data={
                "email": "unknown@example.com",
                "password": "password123",
            },
            request=self.request,
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Correo o contraseña incorrectos.",
            form.non_field_errors(),
        )

    def test_required_fields(self):
        form = LoginForm(
            data={},
            request=self.request,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("password", form.errors)
