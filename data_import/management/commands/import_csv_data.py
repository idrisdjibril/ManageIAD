# data_import/management/commands/import_csv_data.py

from django.core.management.base import BaseCommand
from data_import.tasks import import_csv_data

class Command(BaseCommand):
    help = 'Importe les données CSV dans la base de données'

    def handle(self, *args, **options):
        import_csv_data.delay()
        self.stdout.write(self.style.SUCCESS('Tâche d\'importation des données CSV lancée avec succès'))