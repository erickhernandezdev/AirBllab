from django.contrib import admin
from .models import YubikeyDevice

@admin.register(YubikeyDevice)
class YubikeyDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'public_id', 'confirmed', 'created_at')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('user__email', 'user__username', 'name', 'public_id')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'name')
        }),
        ('Detalles de Yubikey', {
            'fields': ('public_id', 'confirmed'),
            'description': 'Para obtener el Public ID: inserta tu Yubikey, presiona el botón en un editor de texto, y copia los primeros 12 caracteres del OTP generado.'
        }),
        ('Metadatos', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.public_id and len(obj.public_id) > 12:
            obj.public_id = obj.public_id[:12]
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).using('default')