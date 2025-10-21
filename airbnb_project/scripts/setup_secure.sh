#!/bin/bash

echo "Configurando proyecto con medidas de seguridad..."

# Verificar que estamos en el entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
  echo "Error: No estás en un entorno virtual. Por favor, activa tu entorno virtual e intenta de nuevo."
  exit 1
fi

# Instalar dependencias de seguridad
echo "Instalando dependencias de seguridad..."
pip install -r requirements.txt

# Crear variables de entorno
if [ ! -f .env ]; then
  echo "Creando archivo .env con variables de entorno..."
  cat > .env << EOL

# Django
DEBUG=True
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_NAME=airbnb_secure
DB_USER=airbnb_user
DB_PASSWORD=$(openssl rand -base64 32)
DB_HOST=localhost
DB_PORT=5432

# Seguridad
ECRYPTION_KEY=$(openssl rand -base64 32)
DJANGO_SETTINGS_MODULE=airbnb_project.settings
EOL
  echo "Archivo .env creado."
else
  echo "El archivo .env ya existe."
fi

# Ejecutar migraciones
echo "Creando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
echo "Creando superusuario..."
python manage.py createsuperuser

echo "Configuración completa!"
echo "Recuerda:"
echo " - Configurar PostgreSQL con las credenciales del archivo .env."
echo " - Revisar y ajustar el .env para producción."
echo " - Ejectutar: python manage.py runserver"
