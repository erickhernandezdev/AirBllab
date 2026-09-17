"""
URL configuration for airbnb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.cart.views import (
    AddToCartView,
    ClearCartView,
    RemoveFromCartView,
    RemoveActivityView,
    RemoveServiceView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs de las apps
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('new_proposal/', include('apps.new_proposal.urls')),
    path('my_publications/', include('apps.my_publications.urls')),
    path('', include('apps.homepage.urls')),
    path('listings/', include('apps.listings.urls')),
    path('', include('apps.payment.urls')),
    path('account/', include('apps.login.urls')),
    path('item/', include('apps.item_view.urls')),
    path('', include('apps.core.urls')),
    path('cart/', include('apps.cart.urls')),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path(
        'cart/remove-activity/<int:pk>/',
        RemoveActivityView.as_view(),
        name='remove_activity',
    ),
    path(
        'cart/remove-service/<int:pk>/',
        RemoveServiceView.as_view(),
        name='remove_service',
    ),
    path('history/', include('apps.history.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )