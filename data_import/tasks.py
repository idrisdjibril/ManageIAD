# data_import/tasks.py

import subprocess
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def import_csv_data():
    script_path = settings.BASE_DIR / 'scripts' / 'import_csv_naissances_fosa.sh'
    try:
        subprocess.run(['bash', str(script_path)], check=True)
        logger.info("Importation des données CSV réussie")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur lors de l'importation des données CSV : {e}")