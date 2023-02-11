from django.urls import re_path
from .consumers import GameDataConsumer


websocket_urlpatterns = [
    re_path(r'ws/gamedatareceiver/', GameDataConsumer.as_asgi())
]

urlpatterns = [
]
