from rest_framework import serializers
from .models import Order, OrderItem, Reservation, Coupon, Feedback
from products.models import Menu

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model. Handles nested creation within Order.
    """
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_price = serializers.DecimalField(source='item.price', max_digits=6, decimal_places=2, read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_name', 'quantity', 'item_price']
        read_only_fields = ['id', 'item_name']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model, including nested OrderItems.
    """
    items = OrderItemSerializer(many=True)
    waiter_username = serializers.CharField(source='waiter.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'waiter', 'waiter_username', 'table_number', 'status', 'created_at', 'items']
        read_only_fields = ['waiter', 'status', 'created_at']

    def create(self, validated_data):
        """
        Overrides the create method to handle nested OrderItems.
        """
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        """
        Overrides the update method to handle nested OrderItems.
        This method replaces all existing items with the new list provided.
        """
        items_data = validated_data.pop('items', None)

        # Update other fields on the Order instance
        instance.waiter = validated_data.get('waiter', instance.waiter)
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update or create nested items if they were provided
        if items_data is not None:
            # Clear existing items and add new ones
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
        
        return instance

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reservation model.
    """
    class Meta:
        model = Reservation
        fields = ['id', 'customer', 'table_number', 'date', 'time', 'created_at']
        read_only_fields = ['id', 'created_at']

class CouponSerializer(serializers.ModelSerializer):
    """
    Serializer for the Coupon model.
    """
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount', 'active', 'created_at']
        read_only_fields = ['code', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        source='order',
        queryset=Order.objects.all(),
        write_only=True
    )

    class Meta:
        model = Feedback
        fields = ['order_id', 'rating', 'comments']

    def validate_order_id(self, value):
        order = value
        # Check if the order is in a "completed" status
        if order.status.name != 'completed':
            raise serializers.ValidationError('Feedback can only be submitted for completed orders.')

        # Check if feedback has already been submitted for this order
        if Feedback.objects.filter(order=order).exists():
            raise serializers.ValidationError('Feedback for this order has already been submitted.')

        return value
