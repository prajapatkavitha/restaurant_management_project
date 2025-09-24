from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus, Restaurant, Coupon, Reservation

class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.
    """
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'opening_days']

class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderStatus model.
    """
    class Meta:
        model = OrderStatus
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'item_name', 'item_price', 'quantity']
        read_only_fields = ['order']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, including its items and total price.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'waiter', 'table_number', 'status_name', 'items', 'total_price', 'created_at', 'updated_at']

class CouponSerializer(serializers.ModelSerializer):
    """
    Serializer for the Coupon model.
    """
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'active', 'discount', 'created_at']

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reservation model.
    """
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'customer_username', 'table_number', 'date', 'time', 'created_at']
        read_only_fields = ['customer']
