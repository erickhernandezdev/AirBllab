from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('logout/', views.logout_view, name='logout'),
]