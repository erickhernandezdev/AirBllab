from django.urls import path
from .views import CartView, checkout

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('checkout/', checkout, name='checkout'),
]
