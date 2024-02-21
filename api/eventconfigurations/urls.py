from django.urls import path, include
from rest_framework import routers

from .viewsets.eventconfigurationviewset import EventconfigurationViewSet


router = routers.DefaultRouter()
router.register(r'eventconfiguration', EventconfigurationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
