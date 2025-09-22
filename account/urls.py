from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, CustomTokenObtainPairView, UserUpdateViewSet

router = DefaultRouter()
router.register(r'profile', UserUpdateViewSet, basename='user-profile')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('', include(router.urls)),
]
