from django.shortcuts import render
from ..core.models import Accommodation, Service, Activity

def my_publications(request):
    host_id = 1  # TODO: Reemplazar con el id del usuario autenticado

    properties = Accommodation.objects.filter(host_id=host_id)
    services = Service.objects.filter(host_id=host_id)
    activities = Activity.objects.filter(host_id=host_id)

    all_publications = list(properties) + list(services) + list(activities)

    context = {
        'publications': all_publications
    }

    return render(request, 'my_publications/my_publications.html', context)