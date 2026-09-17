from django.shortcuts import render
from django.urls import reverse

from apps.core.models import Accommodation, Activity, Service


def homepage(request):
    cards = [
        {
            "image": "../../media/accommodations/alojamientos.jpg",
            "alt": "Alojamiento",
            "title": "El lugar perfecto para tu estadía",
            "link": reverse("listing", kwargs={"tipo": "accomodations"}),
        },
        {
            "image": "../../media/activities/experiencias.jpg",
            "alt": "Experiencia",
            "title": "Descubre experiencias únicas",
            "link": reverse("listing", kwargs={"tipo": "experiences"}),
        },
        {
            "image": "../../media/services/servicios.jpg",
            "alt": "Servicios",
            "title": "Agrega extras para tu comodidad",
            "link": reverse("listing", kwargs={"tipo": "services"}),
        },
    ]

    accommodations = Accommodation.objects.filter(status="Aprobado")[:5]
    experiences = Activity.objects.filter(status="Aprobado")[:5]
    services = Service.objects.filter(status="Aprobado")[:5]

    def build_card(item):
        if isinstance(item, Accommodation):
            tipo = "accomodations"
        elif isinstance(item, Activity):
            tipo = "experiences"
        elif isinstance(item, Service):
            tipo = "services"
        else:
            tipo = "unknown"

        return {
            "image": item.image.url if item.image else "../../media/default.png",
            "alt": item.name,
            "title": item.name,
            "price": f"₡{getattr(item, 'price', getattr(item, 'price', 0)):,}",
            "rating": f"{getattr(item, 'rating', 4.5):.1f}",
            "link": reverse("detail", kwargs={"tipo": tipo, "id": item.id}),
        }

    accommodations_cards = [build_card(p) for p in accommodations]
    experiences_cards = [build_card(a) for a in experiences]
    services_cards = [build_card(s) for s in services]

    return render(
        request,
        "homepage.html",
        {
            "cards": cards,
            "accommodations": accommodations_cards,
            "experiences": experiences_cards,
            "services": services_cards,
        },
    )
