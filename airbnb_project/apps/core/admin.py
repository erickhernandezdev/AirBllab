from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    User, UserRole,
    Accommodation, AccommodationType,
    Activity, ActivityType,
    Service, ServiceType,
    Reservation, ReservationService, ReservationActivity,
    Cart, CartService, CartActivity,
    Invoice, InvoiceItem
)

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Accommodation)
admin.site.register(AccommodationType)
admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Reservation)
admin.site.register(ReservationService)
admin.site.register(ReservationActivity)
admin.site.register(Cart)
admin.site.register(CartService)
admin.site.register(CartActivity)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)