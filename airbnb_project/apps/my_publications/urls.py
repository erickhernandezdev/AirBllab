from django.urls import path
from . import views

urlpatterns = [
  path('', views.my_publications, name='my_publications'),
]