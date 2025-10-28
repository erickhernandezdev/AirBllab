from apps.core.models import UserRole, CustomUser, AccommodationType, ActivityType, ServiceType, Accommodation, Activity, Service

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
    Accommodation.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'accomodation_type': tipo,
            'description': f'Descripción de {name}',
            'location': 'Costa Rica',
            'price_per_night': 32000,
            'available_from': '2025-11-01',
            'available_to': '2025-12-31',
            'rating': 4.2,
            'status': 'Aprobado',
        }
    )

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
    Service.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'service_type': tipo_servicio,
            'description': f'Descripción de {name}',
            'price': 16000,
            'rating': 4.4,
            'status': 'Aprobado',
        }
    )

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
    Activity.objects.get_or_create(
        name=name,
        defaults={
            'host': user,
            'activity_type': tipo_activity,
            'description': f'Descripción de {name} en Costa Rica',
            'location': 'Costa Rica',
            'price': 28000,
            'rating': 4.6,
            'status': 'Aprobado',
        }
    )

print("Script ejecutado. Usuario creado:", created)
