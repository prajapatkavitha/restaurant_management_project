from celery import shared_task
from django.db.models import Sum
from .models import Order, OrderItem
from django.utils import timezone
from datetime import timedelta

@shared_task
def generate_daily_report():
    """
    Generates and saves a daily sales report.
    """
    today = timezone.now().date()
    start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))

    orders_today = Order.objects.filter(created_at__range=(start_of_day, end_of_day))
    total_sales = orders_today.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = orders_today.count()

    # Logic to find top-selling item
    # This is a simplified version, as your models are not provided.
    top_item = "Not Implemented"

    # Save the report (You will need to create a SalesReport model)
    # SalesReport.objects.create(date=today, total_sales=total_sales, total_orders=total_orders, top_item=top_item)

    return {
        "date": today.isoformat(),
        "total_orders": total_orders,
        "total_sales": total_sales,
        "top_item": top_item
    }
