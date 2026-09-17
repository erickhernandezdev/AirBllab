from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.utils.dateformat import format

from apps.core.models import (
    Accommodation,
    Service,
    Activity,
    Reservation,
    ReservationService,
    ReservationActivity,
    Cart,
    CartService,
    CartActivity,
)


def item_view(request, tipo, id):
    model_map = {
        "accomodations": Accommodation,
        "services": Service,
        "experiences": Activity,
    }

    if tipo not in model_map:
        return render(request, "404.html", status=404)

    model = model_map[tipo]
    item = get_object_or_404(model, pk=id)

    blocked = []

    if tipo == "accomodations":
        reservations = Reservation.objects.filter(accommodation=item)

        for r in reservations:
            current = r.start_date

            while current <= r.end_date:
                blocked.append(format(current, "Y-m-d"))
                current += timedelta(days=1)

    elif tipo == "services":
        reservations = ReservationService.objects.filter(service=item)

        for r in reservations:
            blocked.append(format(r.date, "Y-m-d"))

    elif tipo == "experiences":
        reservations = ReservationActivity.objects.filter(activity=item)

        for r in reservations:
            blocked.append(format(r.date, "Y-m-d"))

    blocked = sorted(set(blocked))

    already_in_cart = False

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)

            if tipo == "accomodations" and cart.accommodation_id == item.id:
                already_in_cart = True

            elif (
                tipo == "services"
                and CartService.objects.filter(cart=cart, service=item).exists()
            ):
                already_in_cart = True

            elif (
                tipo == "experiences"
                and CartActivity.objects.filter(cart=cart, activity=item).exists()
            ):
                already_in_cart = True

        except Cart.DoesNotExist:
            pass

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
