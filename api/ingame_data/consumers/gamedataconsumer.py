from __future__ import annotations
from typing import List
import log
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User
from api.enums import PermissionLevel

logger = log.Logger()


class GameDataConsumer(JsonWebsocketConsumer):
    clients: List[GameDataConsumer] = []
    master: GameDataConsumer = None

    def __init__(self, *args, **kwargs):
        super(GameDataConsumer, self).__init__(args=args, kwargs=kwargs)
        self.user = AnonymousUser()
        self.permissionlevel = PermissionLevel.UNAUTHORIZED

    def connect(self):
        super().connect()
        self.clients.append(self)
        self.user: User = self.scope["user"]  # is actually UserLazyObject but has same attributes as user
        logger.info(f"{self.user} connected.")
