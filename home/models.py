from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    """
    Model to represent categories for the restaurant menu.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

```
eof

I have created the `MenuCategory` model with a unique `name` field. The next and final steps in the task are to run the migrations to create the new table in your database. You can do this by running the following commands in your terminal:

```bash
python manage.py makemigrations home
python manage.py migrate
