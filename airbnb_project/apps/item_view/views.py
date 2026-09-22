from datetime import timedelta

from django.shortcuts import get_object_or_404, render
from django.utils.dateformat import format
from django.views.decorators.http import require_GET

from apps.core.models import (
    Accommodation,
    Activity,
    Cart,
    CartActivity,
    CartService,
    Reservation,
    ReservationActivity,
    ReservationService,
    Service,
)


def _get_blocked_dates(tipo, item):
    blocked = []

    if tipo == "accomodations":
        for r in Reservation.objects.filter(accommodation=item):
            current = r.start_date
            while current <= r.end_date:
                blocked.append(format(current, "Y-m-d"))
                current += timedelta(days=1)

    elif tipo == "services":
        for r in ReservationService.objects.filter(service=item):
            blocked.append(format(r.date, "Y-m-d"))

    elif tipo == "experiences":
        for r in ReservationActivity.objects.filter(activity=item):
            blocked.append(format(r.date, "Y-m-d"))

    return sorted(set(blocked))


def _is_item_in_cart(user, tipo, item):
    if not user.is_authenticated:
        return False

    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return False

    if tipo == "accomodations":
        return cart.accommodation_id == item.id

    if tipo == "services":
        return CartService.objects.filter(cart=cart, service=item).exists()

    if tipo == "experiences":
        return CartActivity.objects.filter(cart=cart, activity=item).exists()

    return False


@require_GET
def item_view(request, tipo, id):
    model_map = {
        "accomodations": Accommodation,
        "services": Service,
        "experiences": Activity,
    }

    if tipo not in model_map:
        return render(request, "404.html", status=404)

    item = get_object_or_404(model_map[tipo], pk=id)
    blocked = _get_blocked_dates(tipo, item)
    already_in_cart = _is_item_in_cart(request.user, tipo, item)

    return render(
        request,
        "item_view.html",
        {
            "item": item,
            "tipo": tipo,
            "blocked_dates": blocked,
            "already_in_cart": already_in_cart,
        },
    )
