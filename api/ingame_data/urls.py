from django.urls import re_path, path, include
from .consumers import GameDataConsumer
from rest_framework import routers

from .viewsets.eventviewset import EventViewSet

router = routers.DefaultRouter()
router.register(r'event', EventViewSet)

websocket_urlpatterns = [
    re_path(r'ws/gamedatareceiver/', GameDataConsumer.as_asgi())
]

urlpatterns = [
    path('', include(router.urls)),
]
