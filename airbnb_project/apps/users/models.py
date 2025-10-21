from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
  class Role(models.TextChoices):
    ADMIN = 'ADMIN', _('Administrador')
    USER = 'USER', _('Usuario normal')
  
  role = models.CharField(
    max_length=10,
    choices=Role.choices,
    default=Role.USER,
  )
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=15, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  #is_verified = models.BooleanField(default=False)

  # CAmpos para auditoría de seguridad
  last_login_ip = models.GenericIPAddressField(null=True, blank=True)
  #login_attempts = models.IntegerField(default=0)

  # related_name personalizado para evitar conflictos
  groups = models.ManyToManyField(
    'auth.Group',
    verbose_name='groups',
    blank=True,
    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    related_name='customuser_set', # Cambiado de 'user_set' a '
    related_query_name='user',
  )
  user_permissions = models.ManyToManyField(
    'auth.Permission',
    verbose_name='user permissions',
    blank=True,
    help_text='Specific permissions for this user.',
    related_name='customuser_set',  # Cambiado de 'user_set' a 'customuser_set'
    related_query_name='user'
  )

  def __str__(self):
    return f"{self.username} ({self.get_role_display()})"
  
  class Meta:
    permissions = [
      ("can_approve_properties", "Puede aprobar propiedades"),
      ("can_manage_users", "Puede gestionar usuarios"),
    ]
