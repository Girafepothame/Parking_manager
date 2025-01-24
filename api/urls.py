from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingViewSet, SpotViewSet

router = DefaultRouter()
router.register(r'parkings', ParkingViewSet)
router.register(r'spots', SpotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
