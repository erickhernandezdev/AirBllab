FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" appuser

COPY --chown=appuser:appuser requirements.txt /app/
RUN pip install --no-cache-dir --only-binary=:all: --upgrade pip==25.2 \
    && pip install --no-cache-dir --only-binary=:all: -r requirements.txt

COPY --chown=appuser:appuser . /app/

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]