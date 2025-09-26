from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    """
    Model to represent categories for the restaurant menu.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ContactFormSubmission(models.Model):
    """
    Model to store contact form submissions from the contact form API.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Makes the model appear as "Contact Form Submissions" in the Django admin
        verbose_name_plural = "Contact Form Submissions"

    def __str__(self):
        # Human-readable representation of the object
        return self.name
