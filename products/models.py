from django.db import models

class Category(models.Model):
    """
    Represents a category for menu items, e.g., 'Appetizers', 'Main Courses'.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Menu(models.Model):
    """
    Represents a dish on the restaurant's menu.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Establishes a many-to-one relationship with the Category model.
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    """
    Represents a separate item with a name and price.
    Note: This model has similar fields to the Menu model.
    """
    item_name = models.CharField(max_length=150)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name
