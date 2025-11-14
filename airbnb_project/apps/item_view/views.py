import json
from django.shortcuts import render, get_object_or_404
from apps.core.models import Accommodation, Service, Activity, Reservation, ReservationService, ReservationActivity
from django.utils.dateformat import format
from datetime import timedelta

def item_view(request, tipo, id):
    model_map = {
        'accomodations': Accommodation,
        'services': Service,
        'experiences': Activity,
    }

    if tipo not in model_map:
        return render(request, '404.html', status=404)

    model = model_map[tipo]
    item = get_object_or_404(model.objects.using('airbnb_user'), pk=id)

    blocked = []
    if tipo == 'accomodations':
        reservations = Reservation.objects.using('airbnb_user').filter(accommodation=item)
        for r in reservations:
            current = r.start_date
            while current <= r.end_date:
                blocked.append(format(current, 'Y-m-d'))
                current += timedelta(days=1)

    elif tipo == 'services':
        reservations = ReservationService.objects.using('airbnb_user').filter(service=item)
        for r in reservations:
            blocked.append(format(r.date, 'Y-m-d'))

    elif tipo == 'experiences':
        reservations = ReservationActivity.objects.using('airbnb_user').filter(activity=item)
        for r in reservations:
            blocked.append(format(r.date, 'Y-m-d'))

    blocked = sorted(set(blocked))

    return render(request, 'item_view.html', {
        'item': item,
        'tipo': tipo,
        'blocked_dates': blocked,
    })
