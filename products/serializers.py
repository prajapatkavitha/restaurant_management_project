from rest_framework import serializers
from .models import Menu, Category

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.
    """
    class Meta:
        model = Item
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model, including all relevant fields.
    """
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'category']
