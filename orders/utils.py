from django.core.mail import send_mail
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def send_email(subject, message, recipient_list):
    """
    Sends a general email using Django's send_mail function.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        recipient_list (list): A list of recipient email addresses.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully with subject: '{subject}' to {recipient_list}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email with subject: '{subject}'. Error: {e}")
        return False

def send_order_confirmation_email(order):
    """
    Sends an order confirmation email to the customer using the generic send_email function.
    It now uses the unique 'order_id' instead of the internal database 'id'.

    Args:
        order: The Order object to be confirmed.
    """
    # Use order.order_id (the unique, short alphanumeric ID)
    subject = f'Order Confirmation: #{order.order_id}'
    message = f"""
    Hello {order.customer_name},

    Thank you for your order!

    Order Details:
    --------------------
    Order ID: {order.order_id}
    Total Amount: ${order.total_price}
    Status: {order.status}

    Items:
    {", ".join([item.product.name for item in order.order_items.all()])}
    
    We will notify you when your order is ready.

    Sincerely,
    The Restaurant Management Team
    """
    recipient_list = [order.customer_email]

    return send_email(subject, message, recipient_list)
