from django.contrib import admin
from django_otp.admin import OTPAdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

class SecureAdminSite(OTPAdminSite):
    pass

secure_admin_site = SecureAdminSite(name='secure_admin')

for model in apps.get_models():
    try:
        secure_admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass