 # authentication/management/commands/createcustomsuperuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a custom superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        username = input('Username: ')
        email = input('Email: ')
        role = input('Role (directeur/administrateur/agent): ')
        password = input('Password: ')
        password2 = input('Confirm password: ')

        if password != password2:
            self.stdout.write(self.style.ERROR('Passwords do not match'))
            return
        if role not in [choice[0] for choice in User.ROLE_CHOICES]:
            self.stdout.write(self.style.ERROR('Invalid role'))
            return

        User.objects.create_superuser(username=username, email=email, role=role, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))