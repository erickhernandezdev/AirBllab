from django.urls import path
from . import views

urlpatterns = [
    path('get-subtypes/', views.get_subtypes, name='get_subtypes'),
]