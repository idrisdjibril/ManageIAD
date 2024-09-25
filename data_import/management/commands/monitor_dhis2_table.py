from django.core.management.base import BaseCommand
from django.db import connections
from django.conf import settings
import json
import os

class Command(BaseCommand):
    help = 'Prépare les métadonnées de la table DHIS2 pour la pagination'

    def handle(self, *args, **options):
        with connections['default'].cursor() as cursor:
            # Récupérer les noms des colonnes
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'dhis2' 
                ORDER BY ordinal_position
            """)
            columns = [row[0] for row in cursor.fetchall()]

            # Compter le nombre total de lignes
            cursor.execute("SELECT COUNT(*) FROM dhis2")
            total_rows = cursor.fetchone()[0]

        # Préparer les données JSON pour la pagination côté client
        data = {
            'columns': columns,
            'total_rows': total_rows,
        }

        # Sauvegarder les métadonnées dans un fichier JSON
        json_path = os.path.join(settings.BASE_DIR, 'data_import', 'static', 'data_import', 'dhis2_metadata.json')
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        self.stdout.write(self.style.SUCCESS(f'{total_rows} lignes de données préparées pour la pagination'))