from django.http import JsonResponse

from .models import AccommodationType, ActivityType, ServiceType


def get_subtypes(request):
    type_selected = request.GET.get("type")
    subtypes = []

    if type_selected == "Alojamiento":
        subtypes = list(AccommodationType.objects.values_list("name", flat=True))
    elif type_selected == "Servicio":
        subtypes = list(ServiceType.objects.values_list("name", flat=True))
    elif type_selected == "Actividad":
        subtypes = list(ActivityType.objects.values_list("name", flat=True))

    return JsonResponse({"subtypes": subtypes})
