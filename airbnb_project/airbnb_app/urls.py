"""
URL configuration for airbnb_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from apps.login import yubikey_only
from django.conf import settings
from django.conf.urls.static import static
from apps.cart.views import AddToCartView, ClearCartView, RemoveFromCartView, RemoveActivityView, RemoveServiceView

urlpatterns = [
  path('admin/', admin.site.urls),
  #path('', TemplateView.as_view(template_name='home.html'), name='home'),

  # Multifactor 
  # Sobreescribir las vistas FIDO2 para usar solo YubiKeys
  path('account/multifactor/fido2/register/', yubikey_only.YubiRegister.as_view(), name='fido2_register'),
  path('account/multifactor/fido2/authenticate/', yubikey_only.YubiAuthenticate.as_view(), name='fido2_authenticate'),
  # Luego incluir las URLs multifactor normales
  path('account/multifactor/', include('multifactor.urls')),
  # URLs de autenticación 2FA
  #path('account/', include('two_factor.urls')),
  #path('account/', include('two_factor.urls', 'two_factor')),

  # URLs de las apps
  #path('users/', include('apps.users.urls')),
  #path('properties/', include('apps.properties.urls')),
  #path('bookings/', include('apps.bookings.urls')),
  #path('payment/', include('apps.payment.urls')),
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
  path('cart/remove-activity/<int:pk>/', RemoveActivityView.as_view(), name='remove_activity'),
  path('cart/remove-service/<int:pk>/', RemoveServiceView.as_view(), name='remove_service'),
  path('history/', include('apps.history.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)