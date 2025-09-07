from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderView, WaiterOrderViewSet, TopCustomersReportView

router = DefaultRouter()
router.register(r'waiter-orders', WaiterOrderViewSet, basename='waiter-orders')

urlpatterns = [
    path('orders/', OrderView.as_view(), name='orders-list'),
    path('reports/top-customers/', TopCustomersReportView.as_view(), name='top-customers-report'),
    path('', include(router.urls)),
]
