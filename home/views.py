from rest_framework import generics
from products.models import Category
from .serializers import CategorySerializer

class CategoryListAPIView(generics.ListAPIView):
    """
    API view to list all menu categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
