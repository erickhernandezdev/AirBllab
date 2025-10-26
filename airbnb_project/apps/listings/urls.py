from django.urls import path
from . import views

urlpatterns = [
    path('<tipo>/', views.listings_view, name='listing'),
]
