from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from .models import Order, OrderItem, Reservation, Coupon
from .serializers import OrderSerializer, ReservationSerializer, CouponSerializer
from .utils import generate_coupon_code
from account.permissions import IsWaiter, IsCashier, IsManagerOrAdmin

# Custom permission for customers
class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customer users access.
    """
    def has_permission(self, request, view):
        # Assumes the 'role' field exists on the User model
        return request.user and request.user.role == 'customer'

# Create your views here.
class TopCustomersReportView(APIView):
    # Only authenticated manager or admin users can view this report.
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        top_customers = Order.objects.values(
            'waiter__username'  # Using waiter field as a proxy for customer since customer name isn't stored in the Order model.
        ).annotate(
            total_spent=Sum('total')
        ).order_by('-total_spent')[:5]

        # Formatting the output to match the desired example.
        formatted_customers = [
            {'name': customer['waiter__username'], 'total_spent': customer['total_spent']}
            for customer in top_customers
        ]

        return Response({'customers': formatted_customers}, status=status.HTTP_200_OK)

class WaiterOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsWaiter]

    def perform_create(self, serializer):
        # Set the waiter to the current authenticated user
        serializer.save(waiter=self.request.user)

    def get_queryset(self):
        # Filter orders to only show those belonging to the current waiter
        return self.queryset.filter(waiter=self.request.user)

    @action(detail=True, methods=['put'])
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if not new_status or new_status not in Order.StatusChoices.values:
            return Response({'error': 'Invalid status provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationView(generics.CreateAPIView):
    # Only authenticated customer users can create a reservation.
    permission_classes = [IsAuthenticated, IsCustomer]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Reservation confirmed", "reservation_id": serializer.data['id']},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

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
        # Generate a unique code and pass it to the serializer save method
        coupon_code = generate_coupon_code()
        serializer.save(code=coupon_code)
