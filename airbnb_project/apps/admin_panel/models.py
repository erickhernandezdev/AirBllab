from typing import ClassVar

from django.conf import settings
from django.db import models

from apps.core.models import Accommodation, Activity, Service


class ApprovalLog(models.Model):
    APPROVAL_TYPE_CHOICES: ClassVar = [
        ("pending", "Pendiente"),
        ("approved", "Aprobado"),
        ("rejected", "Rechazado"),
    ]

    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approval_logs",
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approval_logs",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approval_logs",
    )
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=APPROVAL_TYPE_CHOICES, default="pending"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro de Aprobación"
        verbose_name_plural = "Registros de Aprobación"
        db_table = 'experiences"."approval_log'

    def __str__(self):
        if self.accommodation:
            return (
                f"Alojamiento: {self.accommodation.name} - {self.get_status_display()}"
            )
        elif self.activity:
            return f"Actividad: {self.activity.name} - {self.get_status_display()}"
        elif self.service:
            return f"Servicio: {self.service.name} - {self.get_status_display()}"
        return f"Aprobación #{self.id}"

    @property
    def item_name(self):
        """Retorna el nombre del item asociado"""
        if self.accommodation:
            return self.accommodation.name
        elif self.activity:
            return self.activity.name
        elif self.service:
            return self.service.name
        return "N/A"

    @property
    def item_type(self):
        """Retorna el tipo de item"""
        if self.accommodation:
            return "accommodation"
        elif self.activity:
            return "activity"
        elif self.service:
            return "service"
        return "unknown"
