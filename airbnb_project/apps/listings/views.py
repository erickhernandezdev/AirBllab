from django.shortcuts import render
from django.http import Http404

def listings_view(request, tipo):
    if tipo == 'accomodations':
        title = "Tu próximo destino te espera"
        subtitle = "Explora alojamientos únicos en los rincones más hermosos de Costa Rica"
        items = []
        banner = 'img/alojamientos/alojamientos.jpg'
    elif tipo == 'experiences':
        title = "Vive momentos que dejan huella"
        subtitle = "Sumérgete en experiencias que transformarán tu vida"
        items = []
        banner = 'img/banner-experiencias.jpg'
    elif tipo == 'services':
        title = "Cuida tu cuerpo, tu tiempo y tu espacio"
        subtitle = "Servicios pensados para tu bienestar, productividad y comodidad personal"
        items = []
        banner = 'img/banner-servicios.jpg'
    else:
        raise Http404("Tipo de listado no válido")

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

    return render(request, 'listings.html', {
        'title': title,
        'subtitle': subtitle,
        'items': items,
        'banner': banner,
        'favorites': favorites,
    })
