#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_interoperabilite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    if sys.argv[1] == 'runserver':
        from django.core.management import call_command
        call_command('import_csv_data')
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()