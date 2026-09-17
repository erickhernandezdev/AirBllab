from django.shortcuts import render
from django.urls import reverse
from django.http import Http404

from apps.core.models import Accommodation, Activity, Service


def build_card(obj, tipo):
    name = getattr(obj, "name", "Sin nombre")

    return {
        "image": obj.image.url if obj.image else "../../media/default.png",
        "alt": name,
        "title": name,
        "price": (
            f"₡{obj.price:,} por noche" if hasattr(obj, "price") else f"₡{obj.price:,}"
        ),
        "rating": f"{obj.rating:.1f}",
        "link": reverse("detail", kwargs={"tipo": tipo, "id": obj.id}),
    }


def listings_view(request, tipo):
    if tipo == "accomodations":
        queryset = Accommodation.objects.filter(status="Aprobado")[:5]
        title = "Tu próximo destino te espera"
        subtitle = (
            "Explora alojamientos únicos en los rincones más hermosos de Costa Rica"
        )
        banner = "../media/banners/banner-alojamientos.jpg"

    elif tipo == "experiences":
        queryset = Activity.objects.filter(status="Aprobado")[:5]
        title = "Vive momentos que dejan huella"
        subtitle = "Sumérgete en experiencias que transformarán tu vida"
        banner = "../media/banners/banner-experiencias.jpg"

    elif tipo == "services":
        queryset = Service.objects.filter(status="Aprobado")[:5]
        title = "Cuida tu cuerpo, tu tiempo y tu espacio"
        subtitle = (
            "Servicios pensados para tu bienestar, productividad y comodidad personal"
        )
        banner = "../media/banners/banner-servicios.jpg"

    else:
        raise Http404("Tipo de listado no válido")

    cards = [build_card(obj, tipo) for obj in queryset]

    sections = [
        {"title": "Cerca de ti", "items": cards},
        {"title": "Disponibles el próximo fin de semana", "items": cards},
        {"title": "Te podrían gustar", "items": cards},
        {"title": "Mejor valorados", "items": cards},
    ]

    return render(
        request,
        "listings.html",
        {
            "title": title,
            "subtitle": subtitle,
            "items": cards,
            "banner": banner,
            "sections": sections,
        },
    )
