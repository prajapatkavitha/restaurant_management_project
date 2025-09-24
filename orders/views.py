from rest_framework import viewsets, mixins, status, generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, Count
from django.utils import timezone
from .models import Order, OrderItem, OrderStatus, Restaurant, Coupon, Reservation, Feedback
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    CouponSerializer,
    ReservationSerializer,
    FeedbackSerializer
)
from .utils import generate_coupon_code
from account.permissions import IsWaiter, IsCashier, IsManagerOrAdmin, IsChef
from products.models import Menu


# Custom permission for customers
class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customer users access.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'customer'


class OrderViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling orders, including their nested items.
    It allows for creation, retrieval, updating, and deletion of orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Overrides the default queryset to filter orders by the current user.
        Staff can see all orders, customers can only see their own.
        """
        if self.request.user.role in ['admin', 'manager', 'waiter', 'cashier', 'chef']:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        """
        Auto-assigns the current user as the customer for a new order.
        Sets the initial status to 'pending'.
        """
        pending_status = OrderStatus.objects.get(name='pending')
        serializer.save(customer=self.request.user, status=pending_status)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Action to update the status of an order.
        This endpoint is only for staff members.
        """
        if self.request.user.role not in ['admin', 'manager', 'waiter', 'chef']:
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        order = get_object_or_404(Order, pk=pk)
        new_status_name = request.data.get('status')
        if not new_status_name:
            return Response(
                {'detail': 'Status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            status_obj = OrderStatus.objects.get(name__iexact=new_status_name)
            order.status = status_obj
            order.save()
            return Response(self.get_serializer(order).data)
        except OrderStatus.DoesNotExist:
            return Response(
                {'detail': 'Invalid status provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class OrderItemViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    A viewset for managing order items.
    Allows for deleting an item from an order.
    Note: For creating/updating items, use the nested serializer in OrderViewSet.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        """
        Only the customer who owns the order can delete an item.
        """
        try:
            instance = self.get_object()
            if instance.order.customer != request.user:
                return Response(
                    {'detail': 'You do not have permission to delete this item.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {'detail': 'Item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

class ReservationViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Overrides the default queryset to filter reservations by the current user.
        Staff can see all reservations, customers can only see their own.
        """
        if self.request.user.role in ['admin', 'manager', 'waiter', 'cashier']:
            return Reservation.objects.all()
        return Reservation.objects.filter(customer=self.request.user)
    
    def perform_create(self, serializer):
        """
        Auto-assigns the current user as the customer for a new reservation.
        """
        serializer.save(customer=self.request.user)

class CouponViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Coupon instances.
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    
    def perform_create(self, serializer):
        """
        Overrides the create method to automatically generate a unique
        coupon code before saving the instance.
        """
        coupon_code = generate_coupon_code()
        serializer.save(code=coupon_code)

class TopCustomersReportView(generics.ListAPIView):
    """
    API view to get a report of the top 5 customers based on their total spending.
    Accessible only by managers and admins.
    """
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get_queryset(self):
        # Calculate the total spent by each customer by summing up the costs of their order items.
        # F() is used to reference model fields directly in the database query.
        return Order.objects.values('customer__username').annotate(
            total_spent=Sum(F('items__quantity') * F('items__item__price'))
        ).order_by('-total_spent')[:5]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        formatted_customers = [
            {'name': customer['customer__username'], 'total_spent': customer['total_spent']}
            for customer in queryset
        ]
        return Response({'customers': formatted_customers}, status=status.HTTP_200_OK)

class WaiterOrderViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for waiters to manage orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsWaiter]

    def perform_create(self, serializer):
        serializer.save(waiter=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(waiter=self.request.user)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        # Here we are using a simplified check for the status
        # In a real app, you would want a more robust check, perhaps from a list of valid statuses
        if not new_status:
            return Response({'error': 'Invalid status provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = OrderStatus.objects.get(name=new_status)
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedbackCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for customers to submit feedback on a completed order.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Assuming the user submitting the feedback is the customer
        order = serializer.validated_data['order']
        if order.customer != request.user:
            return Response(
                {"detail": "You can only leave feedback for orders you placed."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Feedback submitted successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class DashboardAPIView(APIView):
    """
    API endpoint to provide key dashboard metrics for managers.
    """
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request, *args, **kwargs):
        # Calculate the start and end of the current day
        today = timezone.now().date()
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        end_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max().time()))

        # Get orders for the current day
        daily_orders = Order.objects.filter(created_at__range=(start_of_day, end_of_day))

        # Calculate total orders and total revenue
        total_orders = daily_orders.count()
        total_revenue = daily_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Find the top-selling dish of the day
        top_dish = None
        top_selling_item = Menu.objects.annotate(
            total_sold=Count('orderitem')
        ).order_by('-total_sold').first()
        
        if top_selling_item:
            top_dish = top_selling_item.name
        
        # Prepare the response data
        response_data = {
            'total_orders': total_orders,
            'revenue': total_revenue,
            'top_dish': top_dish
        }
        return Response(response_data)
