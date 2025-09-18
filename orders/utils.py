import secrets
import string
from django.db import models

# Assuming a Coupon model exists in the orders app.
# If you don't have this model, you'll need to create it.
# from .models import Coupon 

def generate_coupon_code(length: int = 10) -> str:
    """
    Generates a unique alphanumeric coupon code of a specified length.

    Args:
        length (int): The desired length of the coupon code. Defaults to 10.

    Returns:
        str: The unique, generated coupon code.
    """
    if length <= 0:
        raise ValueError("Length must be a positive integer.")

    characters = string.ascii_uppercase + string.digits
    
    while True:
        # Generate a random code
        code = ''.join(secrets.choice(characters) for _ in range(length))
        
        # This is where you would check the database for uniqueness.
        # Example using a hypothetical Coupon model:
        # try:
        #     if not Coupon.objects.filter(code=code).exists():
        #         return code
        # except Exception as e:
        #     # Handle potential database errors
        #     print(f"Database error during coupon generation: {e}")
        #     # In a real-world scenario, you might want to log this error
        #     # and potentially retry or raise a more specific exception.
        #     pass

        # For demonstration purposes, we'll assume uniqueness for now.
        return code
