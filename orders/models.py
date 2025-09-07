from django.db import models
from django.conf import settings

# Create your models here.
class Order(models.Model):
    # Status choices for an order
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        SERVED = "served", "Served"
    
    # Foreign key to the User model to link an order to a waiter
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    table_number = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} for Table {self.table_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey('products.Menu', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
```
eof
After you've updated the `orders/models.py` file, you need to apply these changes to your database by running the following commands in your terminal:

```bash
python manage.py makemigrations orders
python manage.py migrate
