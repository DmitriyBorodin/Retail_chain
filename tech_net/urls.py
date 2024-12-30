from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .apps import TechNetConfig
from .views import EntityViewSet

app_name = TechNetConfig.name

router = DefaultRouter()
router.register(r"entities", EntityViewSet, basename="entity")

urlpatterns = [
    path("", include(router.urls)),
]
