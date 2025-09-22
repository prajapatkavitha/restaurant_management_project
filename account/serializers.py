from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profiles.
    Exposes only the fields that are safe for a user to update themselves.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username'] # Optionally make username read-only

    def validate_email(self, value):
        """
        Check if the email is not already in use by another user.
        """
        user = self.context['request'].user
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
