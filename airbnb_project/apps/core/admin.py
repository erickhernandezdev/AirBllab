from django.contrib import admin

# Register your models here.
from .models import (
    Accommodation,
    AccommodationType,
    Activity,
    ActivityType,
    Cart,
    CartActivity,
    CartService,
    CustomUser,
    Invoice,
    InvoiceItem,
    Reservation,
    ReservationActivity,
    ReservationService,
    Service,
    ServiceType,
    UserRole,
)

admin.site.register(CustomUser)
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
