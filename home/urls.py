from django.urls import path, include
from django.contrib import admin
from .views import CategoryListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/categories/', CategoryListAPIView.as_view(), name='category-list-api'),
    path('api/contact/', include('contact.urls')),
]
