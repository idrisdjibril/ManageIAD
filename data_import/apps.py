from django.apps import AppConfig
from django.core.management import call_command
import threading
import os

class DataImportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_import'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            def run_import_script():
                call_command('start_import_script')

            def monitor_dhis2_table():
                call_command('monitor_dhis2_table')

            threading.Timer(5, run_import_script).start()
            threading.Timer(5, monitor_dhis2_table).start()