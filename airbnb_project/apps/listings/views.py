from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from apps.core.models import Accommodation, Activity, Service

def build_card(obj, image_dict, tipo):
    name = getattr(obj, 'name', 'Sin nombre')
    return {
        'image': image_dict.get(name, image_dict['default']),
        'alt': name,
        'title': name,
        'price': f"₡{obj.price_per_night:,} por noche" if hasattr(obj, 'price_per_night') else f"₡{obj.price:,}",
        'rating': f"{obj.rating:.1f}",
        'link': reverse('detail', kwargs={'tipo': tipo, 'id': obj.id})
    }

def listings_view(request, tipo):
    if tipo == 'accomodations':
        queryset = Accommodation.objects.filter(status='Aprobado')[:5]
        image_dict = {
            'Villa en Tamarindo': 'img/alojamientos/alojamientos.jpg',
            'Casa Don Quijote': 'img/alojamientos/alojamientos2.jpg',
            'Alojamiento en La Fortuna': 'img/alojamientos/alojamientos5.jpg',
            'Villa en Cahuita': 'img/alojamientos/alojamientos4.jpeg',
            'Apartamento en Liberia': 'img/alojamientos/alojamientos3.jpg',
            'default': 'img/alojamientos/alojamientos.jpg'
        }
        title = "Tu próximo destino te espera"
        subtitle = "Explora alojamientos únicos en los rincones más hermosos de Costa Rica"
        banner = 'img/alojamientos/alojamientos.jpg'

    elif tipo == 'experiences':
        queryset = Activity.objects.filter(status='Aprobado')[:5]
        image_dict = {
            'Tour en bote': 'img/experiencias/experiencias.jpg',
            'Clases de cocina': 'img/experiencias/experiencias2.jpg',
            'Clases de fotografia': 'img/experiencias/experiencias3.jpg',
            'Canopy': 'img/experiencias/experiencias4.jpg',
            'Clases de baile': 'img/experiencias/experiencias5.png',
            'default': 'img/experiencias/experiencias.jpg'
        }
        title = "Vive momentos que dejan huella"
        subtitle = "Sumérgete en experiencias que transformarán tu vida"
        banner = 'img/experiencias/experiencias.jpg'

    elif tipo == 'services':
        queryset = Service.objects.filter(status='Aprobado')[:5]
        image_dict = {
            'Catering': 'img/servicios/servicios.jpg',
            'Spa': 'img/servicios/servicios2.jpeg',
            'Masajes': 'img/servicios/servicios3.jpg',
            'Maquillaje': 'img/servicios/servicios4.jpg',
            'Chef personal': 'img/servicios/servicios5.jpg',
            'default': 'img/servicios/servicios.jpg'
        }
        title = "Cuida tu cuerpo, tu tiempo y tu espacio"
        subtitle = "Servicios pensados para tu bienestar, productividad y comodidad personal"
        banner = 'img/servicios/servicios.jpg'

    else:
        raise Http404("Tipo de listado no válido")

    cards = [build_card(obj, image_dict, tipo) for obj in queryset]

    sections = [
        {'title': 'Cerca de ti', 'items': cards},
        {'title': 'Disponibles el próximo fin de semana', 'items': cards},
        {'title': 'Te podrían gustar', 'items': cards},
        {'title': 'Mejor valorados', 'items': cards},
    ]

    return render(request, 'listings.html', {
        'title': title,
        'subtitle': subtitle,
        'items': cards,
        'banner': banner,
        'sections': sections,
    })
