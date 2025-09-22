from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderView,
    WaiterOrderViewSet,
    ReservationView,
    TopCustomersReportView,
    CouponViewSet,
)

# Create a router instance to handle ViewSets
router = DefaultRouter()
# Register the WaiterOrderViewSet under a more general 'orders' path
router.register(r'orders', WaiterOrderViewSet, basename='order')
router.register(r'coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    # Router URLs for the ViewSets
    path('', include(router.urls)),

    # URLs for the specific APIView and generics views
    path('reservations/', ReservationView.as_view(), name='reservation-create'),
    path('reports/top-customers/', TopCustomersReportView.as_view(), name='top-customers-report'),
]
