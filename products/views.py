from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.cache import cache
from django.db.models import Count

from .models import Item, Menu, Category
from .serializers import ItemSerializer, MenuSerializer
from account.permissions import IsManagerOrAdmin
from orders.models import OrderItem

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
    
class PopularDishesReportView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    
    def get(self, request):
        popular_dishes = OrderItem.objects.values(
            'item__name'
        ).annotate(
            orders=Count('id')
        ).order_by('-orders')[:5]
        
        # Format the output to match the desired example
        formatted_dishes = [
            {'dish': dish['item__name'], 'orders': dish['orders']}
            for dish in popular_dishes
        ]
        
        return Response(formatted_dishes, status=status.HTTP_200_OK)

class MenuCategoryListView(generics.ListAPIView):
    """
    API view to list menu items, with an option to filter by category.
    
    Example usage:
    GET /api/menu/by-category/?category=Appetizers
    """
    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Optionally filters menu items by category name provided in a query parameter.
        """
        queryset = Menu.objects.all()
        category_name = self.request.query_params.get('category', None)
        
        if category_name is not None:
            try:
                category = Category.objects.get(name=category_name)
                queryset = queryset.filter(category=category)
            except Category.DoesNotExist:
                # If the category does not exist, return an empty queryset
                queryset = Menu.objects.none()

        return queryset
