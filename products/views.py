from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .models import Item, Menu
from .serializers import ItemSerializer, MenuSerializer
from account.permissions import IsManagerOrAdmin

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().select_related('category')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

class ItemView(APIView):
    # This line applies the permissions to both GET and POST requests.
    # Users must be authenticated, and their role must be Admin or Manager.
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
