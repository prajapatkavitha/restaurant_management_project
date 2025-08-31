from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsWaiter, IsCashier
from .models import Order
from .serializers import OrderSerializer

'''
NOTE: Consider this as a reference and follow this same coding structure or format to work on your tasks
'''

# Create your views here.
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
