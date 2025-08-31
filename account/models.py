# account/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Choices for user roles
    class Role(models.TextChoices):
        ADMIN = "Admin", "Admin"
        MANAGER = "Manager", "Manager"
        CASHIER = "Cashier", "Cashier"
        WAITER = "Waiter", "Waiter"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.WAITER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
