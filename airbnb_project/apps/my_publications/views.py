from django.shortcuts import render
from ..core.models import Accommodations, Services, Activities

def my_publications(request):
  host_id = 1  # TODO: Reemplazar con el id del usuario autenticado

  accommodations = Accommodations.objects.filter(host_id=host_id)
  services = Services.objects.filter(host_id=host_id)
  activities = Activities.objects.filter(host_id=host_id)

  all_publications = list(accommodations) + list(services) + list(activities)
  
  context = {
    'publications': all_publications
  }

  return render(request, 'my_publications/my_publications.html', context)
