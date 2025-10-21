from django.db import models
from django.conf import settings
from apps.properties.models import Property, Activity

class ApprovalLog(models.Model):
  APPROVAL_TYPE_CHOICES = [
    ('pending', 'Pendiente'),
    ('approved', 'Aprobado'),
    ('rejected', 'Rechazado'),
  ]

  property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
  activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
  admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  status = models.CharField(max_length=10, choices=APPROVAL_TYPE_CHOICES, default='pending')
  notes = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Registro de Aprobación'
    verbose_name_plural = 'Registros de Aprobación'

  def __str__(self):
    if self.property:
      return f"{self.property.name} - {self.status}"
    elif self.activity:
      return f"{self.activity.name} - {self.status}"
    return f"Aprobación #{self.id}"
  