from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    """
    Model to represent categories for the restaurant menu.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
        
python manage.py makemigrations home
python manage.py migrate

