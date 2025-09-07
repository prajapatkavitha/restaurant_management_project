from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache

from .models import Item, Menu
from .serializers import ItemSerializer, MenuSerializer
from account.permissions import IsManagerOrAdmin

class ItemView(APIView):
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

class PopularMenuView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        cache_key = 'popular_menu_items'
        
        # Try to get data from the cache
        items = cache.get(cache_key)

        if not items:
            # If not in cache, fetch from the database
            items = Menu.objects.order_by('-order_count')[:5] 
            
            # Cache the data for 5 minutes (300 seconds)
            cache.set(cache_key, items, 300)
            
        serializer = MenuSerializer(items, many=True)
        return Response(serializer.data)

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().select_related('category')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
