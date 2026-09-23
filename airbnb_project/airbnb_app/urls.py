"""
URL configuration for airbnb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from apps.cart.views import (
    AddToCartView,
    ClearCartView,
    RemoveActivityView,
    RemoveFromCartView,
    RemoveServiceView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLs de las apps
    path("admin-panel/", include("apps.admin_panel.urls")),
    path("new_proposal/", include("apps.new_proposal.urls")),
    path("my_publications/", include("apps.my_publications.urls")),
    path("", include("apps.homepage.urls")),
    path("listings/", include("apps.listings.urls")),
    path("", include("apps.payment.urls")),
    path("account/", include("apps.login.urls")),
    path("item/", include("apps.item_view.urls")),
    path("", include("apps.core.urls")),
    path("cart/", include("apps.cart.urls")),
    path("cart/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/clear/", ClearCartView.as_view(), name="clear_cart"),
    path("cart/remove/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path(
        "cart/remove-activity/<int:pk>/",
        RemoveActivityView.as_view(),
        name="remove_activity",
    ),
    path(
        "cart/remove-service/<int:pk>/",
        RemoveServiceView.as_view(),
        name="remove_service",
    ),
    path("history/", include("apps.history.urls")),
]

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
