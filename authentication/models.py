from django.contrib.auth.models import AbstractUser
from django.db import models
from django_otp.models import Device

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('director', 'Directeur'),
        ('admin', 'Administrateur'),
        ('agent', 'Agent'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='agent')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)

    def is_director(self):
        return self.user_type == 'director'

    def is_admin(self):
        return self.user_type == 'admin'

    def is_agent(self):
        return self.user_type == 'agent'

    def __str__(self):
        return self.username

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"