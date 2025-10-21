from django.db import models
from django.conf import settings

class PropertyType(models.TextChoices):
  COMPLETE_STAY = 'COMPLETE', 'Estancia completa'
  PRIVATE_ROOM = 'PRIVATE', 'Habitación privada'
  SHARED_ROOM = 'SHARED', 'Habitación compartida'
  UNIQUE_STAY = 'UNIQUE', 'Alojamiento único'

class Property(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField()
  property_type = models.CharField(
    max_length=10,
    choices=PropertyType.choices
  )
  price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
  location = models.CharField(max_length=200)
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='properties'
  )
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  # Campos para auditoría
  approved_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='approved_properties'
  )
  approved_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return f"{self.name} - {self.get_property_type_display()}"
  
class Activity(models.Model):
  class ActivityType(models.TextChoices):
    LOCAL_TOUR = 'TOUR', 'Tour local'
    CLASS = 'CLASS', 'Clase'
    IMMERSIVE = 'IMMERSIVE', 'Experiencia inmersiva'
    ONLINE = 'ONLINE', 'Experiencia en línea'
  
  name = models.CharField(max_length=200)
  description = models.TextField()
  activity_type = models.CharField(
    max_length=10,
    choices=ActivityType.choices
  )
  price = models.DecimalField(max_digits=10, decimal_places=2)
  provider = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='activities'
  )
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return self.name
