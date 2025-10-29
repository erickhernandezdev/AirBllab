# reservation-system

## Descripción del Proyecto

Este es como un sistema web de reservas de alojamientos y actividades similar a Airbnb, desarrollado con Django.

### Guía de Instalación y ejecución

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual 
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear arhivo de configuración .env con configuraciones

#Crea migraciones
python manage.py makemigrations users properties

# Aplicar migraciones
python manage.py migrate

# Crear usuario administrador
python manage.py createsuperuser

# Ejecutar el servidor
python manage.py runserver

# Para salirse del venv
deactivate

```

Se accede al sistema con los siguientes links:

Sitio principal: <http://127.0.0.1:8000>
Panel de administración: <http://127.0.0.1:8000/admin>
Login: <http://127.0.0.1:8000/login>
