from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrajetViewSet

router = DefaultRouter()
router.register(r'trajets', TrajetViewSet, basename='trajet')

urlpatterns = [
    path('', include(router.urls)),
]