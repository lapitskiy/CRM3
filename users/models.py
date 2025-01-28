from django.contrib.auth.models import User
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Название компании
    created_at = models.DateTimeField(auto_now_add=True)  # Дата регистрации

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.company.name})"