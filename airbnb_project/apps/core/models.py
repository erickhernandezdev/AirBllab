from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado'),
    ('Pendiente', 'Pendiente'),
]
TYPE_CHOICES = [
    ('Alojamiento', 'Alojamiento'),
    ('Actividad', 'Actividad'),
    ('Servicio', 'Servicio'),
]

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Accommodations(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Alojamiento')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
    
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Servicio')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
    
class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Actividad')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
