from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ("Aprobado", "Aprobado"),
    ("Rechazado", "Rechazado"),
    ("Pendiente", "Pendiente"),
]


class UserRole(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users"."roles'


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", _("Administrador")
        USER = "USER", _("Usuario normal")

    user_id = models.AutoField(primary_key=True)
    identity_document = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_role = models.ForeignKey(
        UserRole, on_delete=models.CASCADE, null=True, blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="Rol del usuario en el sistema",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campos para auditoría de seguridad
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar = ["username"]

    # related_name personalizado para evitar conflictos
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="core_customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="core_customuser_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.name or self.username

    @property
    def is_admin(self):
        """Retorna True si el usuario tiene rol de administrador"""
        return self.role == self.Role.ADMIN

    class Meta:
        permissions: ClassVar = [
            ("can_approve_properties", "Puede aprobar propiedades"),
            ("can_manage_users", "Puede gestionar usuarios"),
        ]
        db_table = 'users"."users'


class AccommodationType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'experiences_types"."accommodation_types'


class ActivityType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'experiences_types"."activity_types'


class ServiceType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'experiences_types"."service_types'


class Accommodation(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accommodation_type = models.ForeignKey(AccommodationType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="accommodations/", blank=True, null=True)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pendiente"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'experiences"."accommodations'


class Reservation(models.Model):
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(
        Accommodation, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservations"."reservations'


class Service(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pendiente"
    )

    class Meta:
        db_table = 'experiences"."services'


class Activity(models.Model):
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="activities/", blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pendiente"
    )

    class Meta:
        db_table = 'experiences"."activities'


class ReservationActivity(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        db_table = 'reservations"."reservation_activities'


class ReservationService(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        db_table = 'reservations"."reservation_services'


class Cart(models.Model):
    user = models.OneToOneField(
        "CustomUser", on_delete=models.CASCADE, related_name="cart"
    )
    accommodation = models.ForeignKey(
        Accommodation, on_delete=models.SET_NULL, null=True, blank=True
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    nights = models.IntegerField(null=True)
    price_total = models.IntegerField(null=True)

    class Meta:
        db_table = 'carts"."carts'


class CartActivity(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    total_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    date = models.DateField(null=True)

    class Meta:
        db_table = 'carts"."cart_activities'


class CartService(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    total_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    date = models.DateField(null=True)

    class Meta:
        db_table = 'carts"."cart_services'


class Invoice(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    paid_at = models.DateTimeField()

    class Meta:
        db_table = 'invoices"."invoices'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'invoices"."invoice_items'
