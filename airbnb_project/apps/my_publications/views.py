from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..core.models import Accommodation, Activity, Service


@login_required
def my_publications(request):
    current_user = request.user

    accommodations = Accommodation.objects.filter(host=current_user)
    services = Service.objects.filter(host=current_user)
    activities = Activity.objects.filter(host=current_user)

    all_publications = list(accommodations) + list(services) + list(activities)

    context = {"publications": all_publications}

    return render(request, "my_publications/my_publications.html", context)
