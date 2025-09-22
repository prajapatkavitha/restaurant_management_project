from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils import timezone

class Restaurant(models.Model):
    """
    A model to represent a single restaurant.
    """
    name = models.CharField(max_length=255, unique=True)
    opening_days = models.CharField(
        max_length=50,
        help_text="Comma-separated list of days (e.g., 'Mon,Tue,Wed,Fri,Sat')"
    )

    def __str__(self):
        return self.name

class OrderStatus(models.Model):
    """
    A model to represent different order statuses.
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARING = 'preparing', 'Preparing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    name = models.CharField(
        max_length=50,
        unique=True,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    def __str__(self):
        return self.name

class ActiveOrderManager(models.Manager):
    """
    Custom manager to filter for active orders.
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            status__name__in=[
                OrderStatus.StatusChoices.PENDING,
                OrderStatus.StatusChoices.PREPARING
            ]
        )

class Order(models.Model):
    """
    Model representing a customer's order.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    table_number = models.IntegerField()
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders_by_status'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager() # The default manager
    active_orders = ActiveOrderManager() # Our custom manager

    @property
    def total_price(self):
        """Calculates the total price of the order by summing up item prices."""
        total = self.items.aggregate(total=Sum(models.F('quantity') * models.F('item__price')))['total']
        return total if total is not None else 0

    def __str__(self):
        return f"Order #{self.id} for Table {self.table_number}"

class OrderItem(models.Model):
    """
    Model representing a single item within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey('products.Menu', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

class Reservation(models.Model):
    """
    A model to represent a reservation.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    table_number = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.customer.username} for Table {self.table_number} on {self.date}"

class Coupon(models.Model):
    """
    A model to represent a coupon code.
    """
    code = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
