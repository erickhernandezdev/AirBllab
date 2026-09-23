from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from .models import AccommodationType, ActivityType, ServiceType


@require_GET
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


@require_http_methods(["GET", "HEAD"])
def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)
