from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('approved/', views.approved_items_list, name='approved_items_list'),
]
