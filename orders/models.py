from django.db import models
from django.db.models import F, Sum, UniqueConstraint
from django.conf import settings
from .utils import generate_coupon_code

# Assuming a `Menu` model exists in the `products` app
# and a `User` model exists in the `account` app.

class OrderStatus(models.Model):
    """
    Model to represent the status of an order (e.g., 'pending', 'completed').
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    """
    Model to represent a customer's order.
    """
    # Assuming the 'role' field exists on the User model
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='served_orders')
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

class OrderItem(models.Model):
    """
    Model for individual items within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('products.Menu', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

class Restaurant(models.Model):
    """
    Model to store general restaurant information, like loyalty points earned per visit.
    """
    name = models.CharField(max_length=255)
    loyalty_points_per_visit = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class Coupon(models.Model):
    """
    Model to represent a coupon code with a discount percentage.
    """
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def __str__(self):
        return f"Coupon: {self.code} - {self.discount_percentage}%"

class Feedback(models.Model):
    """
    Model to store customer feedback for a completed order.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['order'], name='unique_order_feedback')
        ]
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"Feedback for Order #{self.order.id} - Rating: {self.rating}"
