from django.shortcuts import render, get_object_or_404
from apps.core.models import Accommodation, Service, Activity, Reservation
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
    item = get_object_or_404(model, pk=id)

    blocked = []
    if tipo == 'accomodations':
        reservations = Reservation.objects.filter(accommodation=item)
        for r in reservations:
            current = r.start_date
            while current <= r.end_date:
                blocked.append(format(current, 'Y-m-d'))
                current += timedelta(days=1)

    return render(request, 'item_view.html', {
        'item': item,
        'tipo': tipo,
        'blocked_dates': blocked,
    })
