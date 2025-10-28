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

urlpatterns = [
  path('admin/', admin.site.urls),
  #path('', TemplateView.as_view(template_name='home.html'), name='home'),

  # URLs de autenticación 2FA
  #path('account/', include('two_factor.urls')),
  #path('account/', include('two_factor.urls', 'two_factor')),

  # URLs de las apps
  #path('users/', include('apps.users.urls')),
  #path('properties/', include('apps.properties.urls')),
  #path('bookings/', include('apps.bookings.urls')),
  #path('payments/', include('apps.payments.urls')),
  path('admin-panel/', include('apps.admin_panel.urls')),
  path('new_proposal/', include('apps.new_proposal.urls')),
  path('my_publications/', include('apps.my_publications.urls')),
  path('', include('apps.homepage.urls')),
  path('listings/', include('apps.listings.urls')),
  path('account/', include('apps.login.urls')),
]
