from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Menu
from .serializers import MenuSerializer
from account.permissions import IsManagerOrAdmin

class MenuViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Menu instances.

    This ViewSet provides 'list', 'retrieve', 'create', 'update',
    'partial_update', and 'destroy' actions.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    # Permission classes for the viewset
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]

    def update(self, request, *args, **kwargs):
        """
        Handles the PUT and PATCH requests for updating a menu item.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
