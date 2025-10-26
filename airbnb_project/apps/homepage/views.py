from django.shortcuts import render
from django.urls import reverse

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
    return render(request, 'homepage.html', {
        'cards': cards,
        'favorites': favorites,
        'experiences': experiences,
        'services': services,
    })
