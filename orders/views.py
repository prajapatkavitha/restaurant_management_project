from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework import generics
from .models import Order, Reservation
from .serializers import OrderSerializer, ReservationSerializer
from account.permissions import IsWaiter, IsCashier

# Create your views here.
class TopCustomersReportView(APIView):
    # Only authenticated users can view this report.
    permission_classes = [IsAuthenticated]

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

class OrderView(APIView):
    # This line applies the permissions to both GET and POST requests.
    # Users must be authenticated, and their role must be Waiter or Cashier.
    permission_classes = [IsAuthenticated, IsWaiter | IsCashier]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    # Only authenticated users can create a reservation.
    permission_classes = [IsAuthenticated]
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
