from django.db import models
from products.models import Menu

class Order(models.Model):
    # Choices for the order status
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        PREPARING = "Preparing", "Preparing"
        READY = "Ready", "Ready"
        SERVED = "Served", "Served"

    customer_name = models.CharField(max_length=150)
    items = models.ManyToManyField(Menu)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order for {self.customer_name} (Status: {self.status})"
# Create your models here.

