from django.db import models
from django.contrib.auth.models import User
class Business(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="business"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(
        upload_to="business_logos/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
