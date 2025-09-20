import secrets
import string
from django.db import models 

# For demonstration, a placeholder model. In your project, you'll
# likely import your actual Coupon model from a file like models.py.
class Coupon(models.Model):
    """
    A simple model to represent a coupon code.
    """
    code = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

def generate_coupon_code(length: int = 10) -> str:
    """
    Generates a unique alphanumeric coupon code of a specified length by
    checking for its existence in the database.

    Args:
        length (int): The desired length of the coupon code. Must be a positive integer.
                      Defaults to 10.

    Returns:
        str: A unique, randomly generated coupon code.

    Raises:
        ValueError: If the provided length is not a positive integer.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer.")

    characters = string.ascii_uppercase + string.digits
    
    while True:
        # Generate a random code
        code = ''.join(secrets.choice(characters) for _ in range(length))
        
        # Check if the generated code already exists in the database
        if not Coupon.objects.filter(code=code).exists():
            return code
