from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, PopularMenuView

router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')

urlpatterns = [
    path('', include(router.urls)),
    path('menu/popular/', PopularMenuView.as_view(), name='popular-menu'),
]
