# accounts/models.py
from django.db import models

class Business(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True)

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
