from django.urls import path

from . import views

urlpatterns = [
    path("", views.add_new_proposal, name="new_proposal"),
]
