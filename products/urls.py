from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PopularDishesReportView, PopularMenuView, MenuViewSet

router = DefaultRouter()
router.register(r'', MenuViewSet, basename='menu')

urlpatterns = [
    path('popular/', PopularMenuView.as_view(), name='popular-menu'),
    path('reports/popular-dishes/', PopularDishesReportView.as_view(), name='popular-dishes-report'),
    path('', include(router.urls)),
]
