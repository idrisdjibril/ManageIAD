# data_import/apps.py

from django.apps import AppConfig

class DataImportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_import'

    def ready(self):
        try:
            import data_import.signals
        except ImportError:
            pass