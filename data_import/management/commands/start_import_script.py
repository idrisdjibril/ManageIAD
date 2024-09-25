from django.core.management.base import BaseCommand
import subprocess
import os

class Command(BaseCommand):
    help = 'Starts the import_csv_naissances_fosa.sh script'

    def handle(self, *args, **options):
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts', 'import_csv_naissances_fosa.sh')
        subprocess.Popen(['bash', script_path])
        self.stdout.write(self.style.SUCCESS('Started import_csv_naissances_fosa.sh script'))