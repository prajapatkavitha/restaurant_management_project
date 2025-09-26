from django.urls import path
from .views import CategoryListAPIView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('admin/', admin.site.urls),
    path('api/contact/', include('contact.urls')),

]

