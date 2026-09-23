from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Crea los esquemas de PostgreSQL necesarios si no existen"

    def handle(self, *args, **options):
        schemas = [
            "django",
            "carts",
            "experiences",
            "experiences_types",
            "invoices",
            "reservations",
            "users",
        ]
        with connection.cursor() as cursor:
            for schema in schemas:
                quoted_schema = connection.ops.quote_name(schema)
                sql = f"CREATE SCHEMA IF NOT EXISTS {quoted_schema};"
                cursor.execute(sql)  # NOSONAR
                self.stdout.write(
                    self.style.SUCCESS(f"Esquema '{schema}' verificado/creado.")
                )
