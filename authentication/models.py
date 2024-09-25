from django.db import models
from django.contrib.auth.models import AbstractUser

class Authenticate(AbstractUser):
    ROLE_CHOICES = (
        ('directeur', 'Directeur'),
        ('administrateur', 'Administrateur'),
        ('agent', 'Agent'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        db_table = 'authentication_authenticate'
    
class HomePageContent(models.Model):
    title = models.CharField(max_length=200)
    welcome_message = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
