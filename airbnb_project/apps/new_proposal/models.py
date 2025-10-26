from django.db import models

STATUS_CHOICES = [
    ('active', 'aprobado'),
    ('rejected', 'rechazado'),
    ('pending', 'pendiente'),
]
TYPE_CHOICES = [
    ('accomodation', 'alojamiento'),
    ('activity', 'actividad'),
    ('service', 'servicio'),
]

class Accomodations(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='accomodation')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
    
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='accomodation')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
    
class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    host_id = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='accomodation')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name
