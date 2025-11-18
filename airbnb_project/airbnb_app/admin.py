from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

# Create an OTP-enabled admin site
class SecureAdminSite(OTPAdminSite):
    pass

secure_admin_site = SecureAdminSite(name='secure_admin')

# Register all models automatically (Optional but common)
for model in apps.get_models():
    try:
        secure_admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass