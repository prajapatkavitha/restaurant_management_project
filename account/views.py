from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import mixins
from django.contrib.auth import get_user_model
from .serializers import UserUpdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    A ViewSet to allow a user to retrieve and update their own profile.
    Only allows GET and PUT/PATCH methods.
    """
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Returns the object the view is displaying. In this case, it's always the
        logged-in user's profile.
        """
        return self.request.user
