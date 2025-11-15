from django.shortcuts import render
from django.urls import reverse
from apps.core.models import Accommodation, Activity, Service

def homepage(request):
    cards = [
        {
            'image': 'img/alojamientos/alojamientos.jpg',
            'alt': 'Alojamiento',
            'title': 'Encuentra el lugar perfecto para tu estadía',
            'link': reverse('listing', kwargs={'tipo': 'accomodations'})
        },
        {
            'image': 'img/experiencias/experiencias.jpg',
            'alt': 'Experiencia',
            'title': 'Descubre experiencias únicas',
            'link': reverse('listing', kwargs={'tipo': 'experiences'})
        },
        {
            'image': 'img/servicios/servicios.jpg',
            'alt': 'Servicios',
            'title': 'Agrega extras para tu comodidad',
            'link': reverse('listing', kwargs={'tipo': 'services'})
        }
    ]

    accommodations = Accommodation.objects.using('airbnb_user').filter(status='Aprobado')[:5]
    experiences = Activity.objects.using('airbnb_user').filter(status='Aprobado')[:5]
    services = Service.objects.using('airbnb_user').filter(status='Aprobado')[:5]

    accomodation_images = {
        'Villa en Tamarindo': 'img/alojamientos/alojamientos.jpg',
        'Casa Don Quijote': 'img/alojamientos/alojamientos2.jpg',
        'Alojamiento en La Fortuna': 'img/alojamientos/alojamientos5.jpg',
        'Villa en Cahuita': 'img/alojamientos/alojamientos4.jpeg',
        'Apartamento en Liberia': 'img/alojamientos/alojamientos3.jpg',
        'default': 'img/alojamientos/alojamientos.jpg'
    }

    activity_images = {
        'Tour en bote': 'img/experiencias/experiencias.jpg',
        'Clases de cocina': 'img/experiencias/experiencias2.jpg',
        'Clases de fotografia': 'img/experiencias/experiencias3.jpg',
        'Canopy': 'img/experiencias/experiencias4.jpg',
        'Clases de baile': 'img/experiencias/experiencias5.png',
        'default': 'img/experiencias/experiencias.jpg'
    }

    service_images = {
        'Catering': 'img/servicios/servicios.jpg',
        'Spa': 'img/servicios/servicios2.jpeg',
        'Masajes': 'img/servicios/servicios3.jpg',
        'Maquillaje': 'img/servicios/servicios4.jpg',
        'Chef personal': 'img/servicios/servicios5.jpg',
        'default': 'img/servicios/servicios.jpg'
    }

    def build_card(item, image_map, default_image):
        if isinstance(item, Accommodation):
            tipo = 'accomodations'
        elif isinstance(item, Activity):
            tipo = 'experiences'
        elif isinstance(item, Service):
            tipo = 'services'
        else:
            tipo = 'unknown'

        return {
            'image': image_map.get(item.name, default_image),
            'alt': item.name,
            'title': item.name,
            'price': f"₡{getattr(item, 'price', getattr(item, 'price', 0)):,}",
            'rating': f"{getattr(item, 'rating', 4.5):.1f}",
            'link': reverse('detail', kwargs={'tipo': tipo, 'id': item.id})
        }

    accommodations_cards = [build_card(p, accomodation_images, accomodation_images['default']) for p in accommodations]
    experiences_cards = [build_card(a, activity_images, activity_images['default']) for a in experiences]
    services_cards = [build_card(s, service_images, service_images['default']) for s in services]

    return render(request, 'homepage.html', {
        'cards': cards,
        'accommodations': accommodations_cards,
        'experiences': experiences_cards,
        'services': services_cards,
    })
