from rest_framework import serializers
from .models import Menu, Category, Item

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.
    """
    class Meta:
        model = Item
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model, including the category name.
    """
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'category']
