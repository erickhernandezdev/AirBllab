from django.db import models

from django.db import models
from django.conf import settings
from django_otp.models import Device

class YubikeyDevice(Device):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='yubikey_devices'
    )
    
    public_id = models.CharField(
        max_length=12,
        unique=True,
        help_text="Los primeros 12 caracteres de un OTP de Yubikey"
    )
    
    name = models.CharField(
        max_length=64,
        help_text="Nombre para esta Yubikey (ej., 'Yubikey de Trabajo')"
    )
    
    confirmed = models.BooleanField(
        default=True,
        help_text="¿Este dispositivo está confirmado y listo para usar?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Dispositivo Yubikey"
        verbose_name_plural = "Dispositivos Yubikey"
        db_table = 'django"."login_yubikeydevice'
    
    def __str__(self):
        return f"{self.user.email} - {self.name} ({self.public_id})"
    
    def verify_token(self, token):
        from yubico_client import Yubico
        from django.conf import settings
        
        token_public_id = token[:12]
        token_public_id = token_public_id.lower()

        if token_public_id != self.public_id:
            return False
        
        try:
            client = Yubico(
                settings.YUBIKEY_CLIENT_ID,
                settings.YUBIKEY_SECRET_KEY,
                api_urls=settings.YUBIKEY_API_URLS
            )
            
            client.verify(token)
            return True
            
        except Exception as e:
            return False