from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.core.cache import cache
from account.permissions import IsManagerOrAdmin
from .models import Menu
from .serializers import MenuSerializer

class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing menu items.
    Only managers and admins can create, update, or delete menu items.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def list(self, request, *args, **kwargs):
        """
        Custom list method to add caching logic.
        """
        # Define a cache key for the menu items
        cache_key = 'menu_items'
        
        # Try to get the data from the cache first
        cached_data = cache.get(cache_key)

        if cached_data:
            # If data is in the cache, return it with the 'cached' flag
            response_data = {'dishes': cached_data, 'cached': True}
            return Response(response_data)
        
        # If no cached data, fetch from the database
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Extract just the names of the dishes for the response
        dish_names = [item['name'] for item in serializer.data]
        
        # Cache the data for 10 minutes (600 seconds)
        cache.set(cache_key, dish_names, timeout=600)
        
        response_data = {'dishes': dish_names, 'cached': False}
        return Response(response_data)

    def perform_create(self, serializer):
        """
        Clears the cache when a new menu item is created.
        """
        # Save the new menu item
        serializer.save()
        # Invalidate the cache
        cache.delete('menu_items')

    def perform_update(self, serializer):
        """
        Clears the cache when a menu item is updated.
        """
        # Save the updated menu item
        serializer.save()
        # Invalidate the cache
        cache.delete('menu_items')

    def perform_destroy(self, instance):
        """
        Clears the cache when a menu item is deleted.
        """
        instance.delete()
        cache.delete('menu_items')
