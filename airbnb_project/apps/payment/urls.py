from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

urlpatterns = [
  path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='checkout'),
]