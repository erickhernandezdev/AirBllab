from apps.core.models import UserRole, CustomUser, AccommodationType, ActivityType, ServiceType, Accommodation, Activity, Service
from django.core.files import File
import os

accommodations_images_paths = {
    'Villa en Tamarindo': 'img/alojamientos/alojamientos.jpg',
    'Casa Don Quijote': 'img/alojamientos/alojamientos2.jpg',
    'Alojamiento en La Fortuna': 'img/alojamientos/alojamientos5.jpg',
    'Villa en Cahuita': 'img/alojamientos/alojamientos4.jpeg',
    'Apartamento en Liberia': 'img/alojamientos/alojamientos3.jpg',
    'default': 'img/alojamientos/alojamientos.jpg'
}

activities_images_paths = {
    'Tour en bote': 'img/experiencias/experiencias.jpg',
    'Clases de cocina': 'img/experiencias/experiencias2.jpg',
    'Clases de fotografia': 'img/experiencias/experiencias3.jpg',
    'Canopy': 'img/experiencias/experiencias4.jpg',
    'Clases de baile': 'img/experiencias/experiencias5.png',
    'default': 'img/experiencias/experiencias.jpg'
}

services_images_paths = {
    'Catering': 'img/servicios/servicios.jpg',
    'Spa': 'img/servicios/servicios2.jpeg',
    'Masajes': 'img/servicios/servicios3.jpg',
    'Maquillaje': 'img/servicios/servicios4.jpg',
    'Chef personal': 'img/servicios/servicios5.jpg',
    'default': 'img/servicios/servicios.jpg'
}

# Roles
UserRole.objects.get_or_create(name='Admin')
UserRole.objects.get_or_create(name='User')

# Tipos de alojamiento
AccommodationType.objects.get_or_create(name='Estancias completas')
AccommodationType.objects.get_or_create(name='Habitaciones privadas')
AccommodationType.objects.get_or_create(name='Habitaciones compartidas')
AccommodationType.objects.get_or_create(name='Alojamientos únicos')

# Tipos de actividad
ActivityType.objects.get_or_create(name='Tours locales')
ActivityType.objects.get_or_create(name='Clases')
ActivityType.objects.get_or_create(name='Experiencias inmersivas')
ActivityType.objects.get_or_create(name='Experiencias online')

# Tipos de servicio
ServiceType.objects.get_or_create(name='Limpieza')
ServiceType.objects.get_or_create(name='Transporte')
ServiceType.objects.get_or_create(name='Comidas')
ServiceType.objects.get_or_create(name='Servicios premium')

# Usuario de prueba
role = UserRole.objects.get(name='User')
user, created = CustomUser.objects.get_or_create(
    email='erickhh2004@gmail.com',
    defaults={
        'identity_document': '118950645',
        'name': 'Erick Hernandez',
        'username': 'erickhh18',
        'user_role': role,
        'date_of_birth': '2004-01-18',
        'password': 'hola1234',
    }
)

# Alojamientos de prueba
accommodations = [
    'Villa en Tamarindo',
    'Casa Don Quijote',
    'Alojamiento en La Fortuna',
    'Villa en Cahuita',
    'Apartamento en Liberia'
]

tipo = AccommodationType.objects.get(name='Estancias completas')

for name in accommodations:
    obj, created = Accommodation.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'accommodation_type': tipo,
            'description': (
                'Esta es una opcion ideal para quienes buscan comodidad, privacidad y una experiencia autentica en Costa Rica. '
                'Este alojamiento ofrece espacios bien distribuidos, acabados acogedores y una atmosfera tranquila rodeada de naturaleza. '
                'Perfecto para familias, parejas o viajeros que desean relajarse y explorar los paisajes tropicales, '
                'cada estancia esta equipada para brindar confort y funcionalidad durante toda la visita.'
            ),
            'location': 'Costa Rica',
            'price': 32000,
            'available_from': '2025-11-01',
            'available_to': '2025-12-31',
            'rating': 4.2,
            'status': 'Aprobado',
        }
    )

    if created:
        image_path = accommodations_images_paths.get(name, accommodations_images_paths['default'])
        full_path = os.path.join('media', image_path)

        if os.path.exists(full_path):
            with open(full_path, 'rb') as img_file:
                obj.image.save(os.path.basename(image_path), File(img_file), save=True)
        else:
            print(f"Imagen no encontrada para {name}: {full_path}")

# Servicios de prueba
services = [
    'Catering',
    'Spa',
    'Masajes',
    'Maquillaje',
    'Chef personal'
]

tipo_servicio = ServiceType.objects.get(name='Servicios premium')

for name in services:
    obj, created = Service.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'service_type': tipo_servicio,
            'description': (
                'Este es un servicio pensado para complementar tu estadia con comodidad, eficiencia y atencion personalizada. '
                'Ofrecido por anfitriones locales con experiencia, este servicio busca facilitar tu dia a dia y enriquecer tu experiencia en Costa Rica. '
                'Ya sea que necesites asistencia logistica, bienestar, transporte o actividades complementarias, cada servicio esta disenado para responder a tus necesidades con profesionalismo y calidez.'
            ),
            'price': 16000,
            'rating': 4.4,
            'status': 'Aprobado',
        }
    )

    if created:
        image_path = services_images_paths.get(name, services_images_paths['default'])
        full_path = os.path.join('media', image_path)

        if os.path.exists(full_path):
            with open(full_path, 'rb') as img_file:
                obj.image.save(os.path.basename(image_path), File(img_file), save=True)
        else:
            print(f"Imagen no encontrada para {name}: {full_path}")

# Actividades de prueba
activities = [
    'Tour en bote',
    'Clases de cocina',
    'Clases de fotografia',
    'Canopy',
    'Clases de baile'
]

tipo_activity = ActivityType.objects.get(name='Experiencias inmersivas')

for name in activities:
    obj, created = Activity.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'activity_type': tipo_activity,
            'description': (
                'Esta es una experiencia disenada para conectar con la esencia natural y cultural de Costa Rica. '
                'Ideal para quienes buscan aventura, descubrimiento o momentos memorables, esta actividad ofrece una combinacion de paisajes unicos, interaccion local y emociones autenticas. '
                'Cada experiencia esta pensada para dejar huella, ya sea explorando la biodiversidad, participando en tradiciones o disfrutando de entornos espectaculares.'
            ),
            'location': 'Costa Rica',
            'price': 28000,
            'rating': 4.6,
            'status': 'Aprobado',
        }
    )

    if created:
        image_path = activities_images_paths.get(name, activities_images_paths['default'])
        full_path = os.path.join('media', image_path)

        if os.path.exists(full_path):
            with open(full_path, 'rb') as img_file:
                obj.image.save(os.path.basename(image_path), File(img_file), save=True)
        else:
            print(f"Imagen no encontrada para {name}: {full_path}")

print("Script ejecutado. Usuario creado:", created)
