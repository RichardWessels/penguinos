from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = "Clears all data from the database"

    def handle(self, *args, **options):
        # List all models
        models = apps.get_models()
        for model in models:
            self.stdout.write(f"Clearing data from model: {model.__name__}")
            model.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("Successfully cleared all data from the database")
        )
