from celery import shared_task
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from orders.models import Order
from products.models import Menu

@shared_task
def generate_daily_sales_report():
    """
    Celery task to generate and log a daily sales report.
    This task is scheduled to run every night.
    """
    today = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

    # Fetch all orders from the past day
    orders = Order.objects.filter(created_at__range=(start_of_day, end_of_day))

    # Calculate total sales and total orders
    total_sales = orders.aggregate(Sum('total'))['total__sum'] or 0
    total_orders = orders.count()

    # Find the top-selling menu item
    top_item = Menu.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count').first()

    report = {
        'date': today.isoformat(),
        'total_orders': total_orders,
        'total_sales': total_sales,
        'top_item': top_item.name if top_item else 'N/A'
    }

    print("Daily Sales Report:")
    print("--------------------")
    for key, value in report.items():
        print(f"{key}: {value}")
    print("--------------------")

    return report
