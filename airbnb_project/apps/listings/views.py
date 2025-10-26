from django.shortcuts import render
from django.http import Http404

def listings_view(request, tipo):
    favorites = [
        {
            'image': 'img/alojamientos/alojamientos.jpg',
            'alt': 'Villa en Tamarindo',
            'title': 'Villa en Tamarindo',
            'price': '₡80.000 por noche',
            'rating': '4.5',
            'link': '#'
        },
        {
            'image': 'img/alojamientos/alojamientos2.jpg',
            'alt': 'Cabaña Don Quijote',
            'title': 'Cabaña Don Quijote',
            'price': '₡42.000 por noche',
            'rating': '4.2',
            'link': '#'
        },
        {
            'image': 'img/alojamientos/alojamientos5.jpg',
            'alt': 'Alojamiento en La Fortuna',
            'title': 'Alojamiento en La Fortuna',
            'price': '₡61.000 por noche',
            'rating': '5.0',
            'link': '#'
        },
        {
            'image': 'img/alojamientos/alojamientos4.jpeg',
            'alt': 'Villa en Cahuita',
            'title': 'Villa en Cahuita',
            'price': '₡54.000 por noche',
            'rating': '4.5',
            'link': '#'
        },
        {
            'image': 'img/alojamientos/alojamientos3.jpg',
            'alt': 'Apartamento en Jacó',
            'title': 'Apartamento en Jacó',
            'price': '₡46.000 por noche',
            'rating': '4.8',
            'link': '#'
        },
    ]
    experiences = [
        {
            'image': 'img/experiencias/experiencias.jpg',
            'alt': 'Tour en bote',
            'title': 'Tour en bote',
            'price': '₡64.000',
            'rating': '4.8',
            'link': '#'
        },
        {
            'image': 'img/experiencias/experiencias2.jpg',
            'alt': 'Clases de cocina',
            'title': 'Clases de cocina',
            'price': '₡7.000 por clase',
            'rating': '4.1',
            'link': '#'
        },
        {
            'image': 'img/experiencias/experiencias3.jpg',
            'alt': 'Clases de fotografía',
            'title': 'Clases de fotografía',
            'price': '₡5.000 por clase',
            'rating': '4.4',
            'link': '#'
        },
        {
            'image': 'img/experiencias/experiencias4.jpg',
            'alt': 'Canopy',
            'title': 'Canopy',
            'price': '₡28.000',
            'rating': '4.9',
            'link': '#'
        },
        {
            'image': 'img/experiencias/experiencias5.png',
            'alt': 'Clases de baile',
            'title': 'Clases de baile',
            'price': '₡4.000 por clase',
            'rating': '5.0',
            'link': '#'
        },
    ]
    services = [
        {
            'image': 'img/servicios/servicios.jpg',
            'alt': 'Catering',
            'title': 'Catering',
            'price': '₡40.000',
            'rating': '4.8',
            'link': '#'
        },
        {
            'image': 'img/servicios/servicios2.jpeg',
            'alt': 'Spa',
            'title': 'Spa',
            'price': '₡18.000',
            'rating': '4.7',
            'link': '#'
        },
        {
            'image': 'img/servicios/servicios3.jpg',
            'alt': 'Masajes',
            'title': 'Masajes',
            'price': '₡21.000',
            'rating': '4.0',
            'link': '#'
        },
        {
            'image': 'img/servicios/servicios4.jpg',
            'alt': 'Maquillaje',
            'title': 'Maquillaje',
            'price': '₡10.000',
            'rating': '4.1',
            'link': '#'
        },
        {
            'image': 'img/servicios/servicios5.jpg',
            'alt': 'Chef personal',
            'title': 'Chef personal',
            'price': '₡8.000 por día',
            'rating': '4.9',
            'link': '#'
        },
    ]

    if tipo == 'accomodations':
        title = "Tu próximo destino te espera"
        subtitle = "Explora alojamientos únicos en los rincones más hermosos de Costa Rica"
        items = favorites
        banner = 'img/alojamientos/alojamientos.jpg'
        sections = [
            {'title': 'Cerca de ti', 'items': favorites},
            {'title': 'Disponibles el próximo fin de semana', 'items': favorites},
            {'title': 'Lugares para quedarse cerca de Tamarindo', 'items': favorites},
            {'title': 'Mejor valorados', 'items': favorites},
        ]
    elif tipo == 'experiences':
        title = "Vive momentos que dejan huella"
        subtitle = "Sumérgete en experiencias que transformarán tu vida"
        items = experiences
        banner = 'img/experiencias/experiencias.jpg'
        sections = [
            {'title': 'Experiencias cerca de ti', 'items': experiences},
            {'title': 'Para el fin de semana', 'items': experiences},
            {'title': 'Actividades en Tamarindo', 'items': experiences},
            {'title': 'Las más valoradas', 'items': experiences},
        ]
    elif tipo == 'services':
        title = "Cuida tu cuerpo, tu tiempo y tu espacio"
        subtitle = "Servicios pensados para tu bienestar, productividad y comodidad personal"
        items = services
        banner = 'img/servicios/servicios.jpg'
        sections = [
            {'title': 'Servicios cerca de ti', 'items': services},
            {'title': 'Disponibles este fin de semana', 'items': services},
            {'title': 'Servicios en Tamarindo', 'items': services},
            {'title': 'Mejor valorados', 'items': services},
        ]
    else:
        raise Http404("Tipo de listado no válido")

    return render(request, 'listings.html', {
        'title': title,
        'subtitle': subtitle,
        'items': items,
        'banner': banner,
        'favorites': favorites,
        'experiences': experiences,
        'services': services,
        'sections': sections,
    })
