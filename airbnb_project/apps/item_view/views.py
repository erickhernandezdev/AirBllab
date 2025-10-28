from django.shortcuts import render, get_object_or_404
from apps.core.models import Accommodation, Service, Activity

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

    return render(request, 'item_view.html', {
        'item': item,
        'tipo': tipo,
    })
