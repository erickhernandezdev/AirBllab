import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "airbnb_app.settings")
django.setup()

from apps.core.models import (
    UserRole,
    CustomUser,
    AccommodationType,
    ActivityType,
    ServiceType,
    Accommodation,
    Activity,
    Service,
)

ACCOMMODATIONS_IMAGES = {
    "Villa en Tamarindo": "accommodations/alojamientos.jpg",
    "Casa Don Quijote": "accommodations/alojamientos2.jpg",
    "Alojamiento en La Fortuna": "accommodations/alojamientos5.jpg",
    "Villa en Cahuita": "accommodations/alojamientos4.jpeg",
    "Apartamento en Liberia": "accommodations/alojamientos3.jpg",
    "default": "accommodations/alojamientos.jpg",
}

ACTIVITIES_IMAGES = {
    "Tour en bote": "activities/experiencias.jpg",
    "Clases de cocina": "activities/experiencias2.jpg",
    "Clases de fotografia": "activities/experiencias3.jpg",
    "Canopy": "activities/experiencias4.jpg",
    "Clases de baile": "activities/experiencias5.png",
    "default": "activities/experiencias.jpg",
}

SERVICES_IMAGES = {
    "Catering": "services/servicios.jpg",
    "Spa": "services/servicios2.jpeg",
    "Masajes": "services/servicios3.jpg",
    "Maquillaje": "services/servicios4.jpg",
    "Chef personal": "services/servicios5.jpg",
    "default": "services/servicios.jpg",
}


def set_image(obj, image_path):
    """Assign an existing image from media/ without copying it."""
    full_path = os.path.join("media", image_path)

    if os.path.exists(full_path):
        obj.image.name = image_path
        obj.save(update_fields=["image"])
    else:
        print(f"Imagen no encontrada: {full_path}")


# Roles
UserRole.objects.get_or_create(name="Admin")
UserRole.objects.get_or_create(name="User")


# Tipos de alojamiento
AccommodationType.objects.get_or_create(name="Estancias completas")
AccommodationType.objects.get_or_create(name="Habitaciones privadas")
AccommodationType.objects.get_or_create(name="Habitaciones compartidas")
AccommodationType.objects.get_or_create(name="Alojamientos unicos")


# Tipos de actividad
ActivityType.objects.get_or_create(name="Tours locales")
ActivityType.objects.get_or_create(name="Clases")
ActivityType.objects.get_or_create(name="Experiencias inmersivas")
ActivityType.objects.get_or_create(name="Experiencias online")


# Tipos de servicio
ServiceType.objects.get_or_create(name="Limpieza")
ServiceType.objects.get_or_create(name="Transporte")
ServiceType.objects.get_or_create(name="Comidas")
ServiceType.objects.get_or_create(name="Servicios premium")


# Usuario de prueba
user_role = UserRole.objects.get(name="User")

user, user_created = CustomUser.objects.get_or_create(
    email="erickhh2004@gmail.com",
    defaults={
        "identity_document": "118950645",
        "name": "Erick Hernandez",
        "username": "erickhh18",
        "user_role": user_role,
        "date_of_birth": "2004-01-18",
    },
)

if user_created:
    user.set_password("hola1234")
    user.save()


# Alojamientos de prueba
accommodations = [
    "Villa en Tamarindo",
    "Casa Don Quijote",
    "Alojamiento en La Fortuna",
    "Villa en Cahuita",
    "Apartamento en Liberia",
]

accommodation_type = AccommodationType.objects.get(name="Estancias completas")

for name in accommodations:
    accommodation, accommodation_created = Accommodation.objects.get_or_create(
        name=name,
        defaults={
            "host": user,
            "accommodation_type": accommodation_type,
            "description": (
                "Esta es una opcion ideal para quienes buscan comodidad, "
                "privacidad y una experiencia autentica en Costa Rica. "
                "Este alojamiento ofrece espacios bien distribuidos, "
                "acabados acogedores y una atmosfera tranquila rodeada "
                "de naturaleza. Perfecto para familias, parejas o "
                "viajeros que desean relajarse y explorar los paisajes "
                "tropicales, cada estancia esta equipada para brindar "
                "confort y funcionalidad durante toda la visita."
            ),
            "location": "Costa Rica",
            "price": 32000,
            "available_from": "2026-11-01",
            "available_to": "2026-12-31",
            "rating": 4.2,
            "status": "Aprobado",
        },
    )

    if accommodation_created:
        image_path = ACCOMMODATIONS_IMAGES.get(name, ACCOMMODATIONS_IMAGES["default"])
        set_image(accommodation, image_path)


# Servicios de prueba
services = [
    "Catering",
    "Spa",
    "Masajes",
    "Maquillaje",
    "Chef personal",
]

service_type = ServiceType.objects.get(name="Servicios premium")

for name in services:
    service, service_created = Service.objects.get_or_create(
        name=name,
        defaults={
            "host": user,
            "service_type": service_type,
            "description": (
                "Este es un servicio pensado para complementar tu estadia "
                "con comodidad, eficiencia y atencion personalizada. "
                "Ofrecido por anfitriones locales con experiencia, este "
                "servicio busca facilitar tu dia a dia y enriquecer tu "
                "experiencia en Costa Rica. Ya sea que necesites asistencia "
                "logistica, bienestar, transporte o actividades "
                "complementarias, cada servicio esta disenado para responder "
                "a tus necesidades con profesionalismo y calidez."
            ),
            "price": 16000,
            "rating": 4.4,
            "status": "Aprobado",
        },
    )

    if service_created:
        image_path = SERVICES_IMAGES.get(name, SERVICES_IMAGES["default"])
        set_image(service, image_path)


# Actividades de prueba
activities = [
    "Tour en bote",
    "Clases de cocina",
    "Clases de fotografia",
    "Canopy",
    "Clases de baile",
]

activity_type = ActivityType.objects.get(name="Experiencias inmersivas")

for name in activities:
    activity, activity_created = Activity.objects.get_or_create(
        name=name,
        defaults={
            "host": user,
            "activity_type": activity_type,
            "description": (
                "Esta es una experiencia disenada para conectar con la "
                "esencia natural y cultural de Costa Rica. Ideal para "
                "quienes buscan aventura, descubrimiento o momentos "
                "memorables, esta actividad ofrece una combinacion de "
                "paisajes unicos, interaccion local y emociones autenticas. "
                "Cada experiencia esta pensada para dejar huella, ya sea "
                "explorando la biodiversidad, participando en tradiciones "
                "o disfrutando de entornos espectaculares."
            ),
            "location": "Costa Rica",
            "price": 28000,
            "rating": 4.6,
            "status": "Aprobado",
            "image": ACTIVITIES_IMAGES.get(name, ACTIVITIES_IMAGES["default"]),
        },
    )

    if activity_created:
        image_path = ACTIVITIES_IMAGES.get(name, ACTIVITIES_IMAGES["default"])
        set_image(activity, image_path)


print("Script ejecutado correctamente. " f"Usuario creado: {user_created}")
