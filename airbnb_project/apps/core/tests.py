from decimal import Decimal
from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import (
    Activity,
    ActivityType,
    Accommodation,
    AccommodationType,
    Cart,
    CartActivity,
    CartService,
    CustomUser,
    Invoice,
    InvoiceItem,
    Reservation,
    ReservationActivity,
    ReservationService,
    Service,
    ServiceType,
    UserRole,
)


class CustomUserTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.role, CustomUser.Role.USER)

    def test_user_is_not_admin_by_default(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        self.assertFalse(user.is_admin)

    def test_admin_user_is_admin(self):
        user = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="password123",
            name="Admin User",
            role=CustomUser.Role.ADMIN,
        )

        self.assertTrue(user.is_admin)

    def test_user_str(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            name="Test User",
        )

        self.assertEqual(str(user), "Test User")


class AccommodationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host User",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel",
            description="Hotel de prueba",
        )

    def test_create_accommodation(self):
        accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Un hotel de prueba",
            location="San José",
            price=Decimal("50000.00"),
        )

        self.assertEqual(accommodation.name, "Hotel Test")
        self.assertEqual(accommodation.host, self.user)
        self.assertEqual(
            accommodation.accommodation_type,
            self.accommodation_type,
        )

    def test_accommodation_default_status(self):
        accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Un hotel de prueba",
            location="San José",
            price=Decimal("50000.00"),
        )

        self.assertEqual(accommodation.status, "Pendiente")

    def test_accommodation_invalid_status(self):
        accommodation = Accommodation(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Un hotel de prueba",
            location="San José",
            price=Decimal("50000.00"),
            status="InvalidStatus",
        )

        with self.assertRaises(ValidationError):
            accommodation.full_clean()


class UserRoleTest(TestCase):

    def test_create_user_role(self):
        role = UserRole.objects.create(name="Administrador")

        self.assertEqual(role.name, "Administrador")
        self.assertEqual(str(role), "Administrador")


class AccommodationTypeTest(TestCase):

    def test_create_accommodation_type(self):
        accommodation_type = AccommodationType.objects.create(
            name="Hotel",
            description="Hotel de prueba",
        )

        self.assertEqual(str(accommodation_type), "Hotel")
        self.assertEqual(accommodation_type.description, "Hotel de prueba")


class ActivityTypeTest(TestCase):

    def test_create_activity_type(self):
        activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour de prueba",
        )

        self.assertEqual(str(activity_type), "Tour")


class ServiceTypeTest(TestCase):

    def test_create_service_type(self):
        service_type = ServiceType.objects.create(
            name="Transporte",
            description="Servicio de transporte",
        )

        self.assertEqual(str(service_type), "Transporte")


class ActivityTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host User",
        )

        self.activity_type = ActivityType.objects.create(
            name="Tour",
            description="Tour de prueba",
        )

    def test_create_activity(self):
        activity = Activity.objects.create(
            host=self.user,
            activity_type=self.activity_type,
            name="Tour por San José",
            description="Tour de prueba",
            location="San José",
            price=Decimal("25000.00"),
        )

        self.assertEqual(activity.name, "Tour por San José")
        self.assertEqual(activity.host, self.user)
        self.assertEqual(activity.activity_type, self.activity_type)
        self.assertEqual(activity.price, Decimal("25000.00"))


class ServiceTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host User",
        )

        self.service_type = ServiceType.objects.create(
            name="Transporte",
            description="Servicio de transporte",
        )

    def test_create_service(self):
        service = Service.objects.create(
            host=self.user,
            service_type=self.service_type,
            name="Transporte privado",
            description="Servicio de transporte",
            price=Decimal("15000.00"),
        )

        self.assertEqual(service.name, "Transporte privado")
        self.assertEqual(service.host, self.user)
        self.assertEqual(service.service_type, self.service_type)
        self.assertEqual(service.price, Decimal("15000.00"))


class ReservationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="guest",
            email="guest@example.com",
            password="password123",
            name="Guest User",
        )

        self.host = CustomUser.objects.create_user(
            username="host",
            email="host@example.com",
            password="password123",
            name="Host User",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel",
        )

        self.accommodation = Accommodation.objects.create(
            host=self.host,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Hotel de prueba",
            location="San José",
            price=Decimal("50000.00"),
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            guest=self.user,
            accommodation=self.accommodation,
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 5),
            status="Pendiente",
        )

        self.assertEqual(reservation.guest, self.user)
        self.assertEqual(reservation.accommodation, self.accommodation)
        self.assertEqual(reservation.start_date, date(2026, 10, 1))
        self.assertEqual(reservation.end_date, date(2026, 10, 5))


class CartTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="Test User",
        )

    def test_create_cart(self):
        cart = Cart.objects.create(
            user=self.user,
            nights=3,
            price_total=150000,
        )

        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.nights, 3)
        self.assertEqual(cart.price_total, 150000)

    def test_user_has_one_cart(self):
        cart = Cart.objects.create(user=self.user)

        self.assertEqual(self.user.cart, cart)


class ReservationActivityTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        activity_type = ActivityType.objects.create(name="Tour")

        activity = Activity.objects.create(
            host=self.user,
            activity_type=activity_type,
            name="Tour Test",
            description="Tour",
            location="San José",
            price=Decimal("20000.00"),
        )

        self.reservation = Reservation.objects.create(
            guest=self.user,
            status="Pendiente",
        )

        self.activity = activity

    def test_create_reservation_activity(self):
        item = ReservationActivity.objects.create(
            reservation=self.reservation,
            activity=self.activity,
            total_price=Decimal("20000.00"),
            date=date(2026, 10, 1),
        )

        self.assertEqual(item.reservation, self.reservation)
        self.assertEqual(item.activity, self.activity)
        self.assertEqual(item.total_price, Decimal("20000.00"))


class ReservationServiceTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        service_type = ServiceType.objects.create(name="Transporte")

        self.service = Service.objects.create(
            host=self.user,
            service_type=service_type,
            name="Transporte Test",
            description="Servicio",
            price=Decimal("15000.00"),
        )

        self.reservation = Reservation.objects.create(
            guest=self.user,
            status="Pendiente",
        )

    def test_create_reservation_service(self):
        item = ReservationService.objects.create(
            reservation=self.reservation,
            service=self.service,
            total_price=Decimal("15000.00"),
            date=date(2026, 10, 1),
        )

        self.assertEqual(item.reservation, self.reservation)
        self.assertEqual(item.service, self.service)
        self.assertEqual(item.total_price, Decimal("15000.00"))


class InvoiceTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        self.reservation = Reservation.objects.create(
            guest=self.user,
            status="Pendiente",
        )

    def test_create_invoice(self):
        invoice = Invoice.objects.create(
            reservation=self.reservation,
            amount=Decimal("50000.00"),
            payment_method="Tarjeta",
            paid_at="2026-10-01T12:00:00Z",
        )

        self.assertEqual(invoice.reservation, self.reservation)
        self.assertEqual(invoice.amount, Decimal("50000.00"))
        self.assertEqual(invoice.payment_method, "Tarjeta")


class InvoiceItemTest(TestCase):

    def test_create_invoice_item(self):
        user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="User",
        )

        reservation = Reservation.objects.create(
            guest=user,
            status="Pendiente",
        )

        invoice = Invoice.objects.create(
            reservation=reservation,
            amount=Decimal("50000.00"),
            payment_method="Tarjeta",
            paid_at="2026-10-01T12:00:00Z",
        )

        item = InvoiceItem.objects.create(
            invoice=invoice,
            quantity=2,
            unit_price=Decimal("25000.00"),
            total=Decimal("50000.00"),
        )

        self.assertEqual(item.invoice, invoice)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.total, Decimal("50000.00"))

class ModelRelationshipsTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user",
            email="user@example.com",
            password="password123",
            name="Test User",
        )

        self.accommodation_type = AccommodationType.objects.create(
            name="Hotel"
        )

        self.accommodation = Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel Test",
            description="Hotel de prueba",
            location="San José",
            price=Decimal("50000.00"),
        )

    def test_user_can_have_multiple_accommodations(self):
        Accommodation.objects.create(
            host=self.user,
            accommodation_type=self.accommodation_type,
            name="Hotel 2",
            description="Otro hotel",
            location="Alajuela",
            price=Decimal("40000.00"),
        )

        self.assertEqual(
            Accommodation.objects.filter(host=self.user).count(),
            2,
        )

    def test_deleting_user_deletes_accommodations(self):
        self.user.delete()

        self.assertEqual(
            Accommodation.objects.count(),
            0,
        )

    def test_deleting_accommodation_sets_reservation_to_null(self):
        reservation = Reservation.objects.create(
            guest=self.user,
            accommodation=self.accommodation,
            status="Pendiente",
        )

        self.accommodation.delete()
        reservation.refresh_from_db()

        self.assertIsNone(reservation.accommodation)