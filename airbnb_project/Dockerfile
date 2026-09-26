FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

COPY requirements.txt /app/
RUN pip install --no-cache-dir --only-binary=:all: --require-hashes -r requirements.txt

COPY airbnb_app /app/airbnb_app
COPY apps /app/apps
COPY templates /app/templates
COPY static /app/static
COPY utils /app/utils
COPY manage.py /app/

COPY --chown=appuser:appuser media /app/media

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]