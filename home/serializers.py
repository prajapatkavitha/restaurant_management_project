from rest_framework import serializers
from .models import MenuCategory, ContactFormSubmission

class MenuCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the MenuCategory model.
    """
    class Meta:
        model = MenuCategory
        fields = ['id', 'name']

class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for handling incoming contact form data and converting it
    to and from the ContactFormSubmission model instance.
    """
    class Meta:
        model = ContactFormSubmission
        fields = ['id', 'name', 'email', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
