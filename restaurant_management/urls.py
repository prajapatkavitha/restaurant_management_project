from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # DRF login/logout for browsable API
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints for each app
    path('api/home/', include('home.urls')),
    path('api/accounts/', include('account.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
]

