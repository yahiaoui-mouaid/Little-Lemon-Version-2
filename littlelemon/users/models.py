from django.db import models
from django.contrib.auth.models import AbstractUser


# 3 roles: Customer, Manager, Delivery Crew
class CustomUser(AbstractUser):
    # Define the choices (The "Sticker Colors")
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('MANAGER', 'Manager'),
        ('DELIVERY', 'Delivery Crew'),
    )
    
    # Add the role field to the ID badge
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    def __str__(self):
        return f"{self.username} - {self.role}"
    

    