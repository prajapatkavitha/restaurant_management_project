from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderView, WaiterOrderViewSet

router = DefaultRouter()
router.register(r'waiter-orders', WaiterOrderViewSet, basename='waiter-orders')

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders-list'),
    path('', include(router.urls)),
]
