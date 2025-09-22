from django.core.mail import send_mail
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def send_order_confirmation_email(order):
    """
    Sends an order confirmation email to the customer.

    Args:
        order: The Order object to be confirmed.
    """
    subject = f'Order Confirmation: #{order.id}'
    message = f"""
    Hello {order.customer_name},

    Thank you for your order!

    Order Details:
    --------------------
    Order ID: {order.id}
    Total Amount: ${order.total_price}
    Status: {order.status}

    Items:
    {", ".join([item.product.name for item in order.order_items.all()])}
    
    We will notify you when your order is ready.

    Sincerely,
    The Restaurant Management Team
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.customer_email]

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Order confirmation email sent successfully for Order #{order.id} to {order.customer_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email for Order #{order.id} to {order.customer_email}. Error: {e}")
        return False
