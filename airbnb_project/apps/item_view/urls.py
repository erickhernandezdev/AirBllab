from django.urls import path
from . import views

urlpatterns = [
    path('<str:tipo>/<int:id>/', views.item_view, name='detail'),
]
