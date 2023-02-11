from __future__ import annotations

import datetime
import re
from typing import List

from django.contrib.auth import authenticate
from jsonschema.exceptions import ValidationError

import log
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser, User
from api.enums import PermissionLevel
from api.ingame_data.consumers.validators.validators import Validators
from api.ingame_data.objectmapping import objectmapping
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

    def receive_json(self, content, **kwargs):
        try:
            Validators.validateJson(content.get('type', None), content)
        except ValidationError as e:
            self.send_json({'type': 'error', 'command': content.get('type', None), 'msg': e.message})
            return
        actiontype = content.get('type')
        data = content.get('data', {})

        if actiontype == "login":
            self.login(data.get("username"), data.get("password"))
        elif actiontype == "logout":
            self.logout()
        elif actiontype == "event":
            self.ingame_event(content)
        elif actiontype == "requestmaster":
            self.requestMaster()

    def login(self, username, password):
        user = authenticate(username=username, password=password)

        if user is not None:
            logger.info(f"{user} logged in.")
            self.user = user
            if self.user.is_superuser:
                self.permissionlevel = PermissionLevel.ADMINISTRATOR
            else:
                self.permissionlevel = PermissionLevel.LOGGED_IN
            self.send_json({"type": "success", "command": "login", "msg": "success",
                            "permissionlevel": self.permissionlevel.value})
        else:
            self.send_json({"type": "error", "command": "login", "msg": "Invalid credentials"})

    def logout(self):
        logger.info(f"{self.user} logged out")
        self.user = AnonymousUser()
        self.permissionlevel = PermissionLevel.UNAUTHORIZED
        self.send_json({"type": "success", "command": "logout", "msg": "Successfully logged out"})

    def requestMaster(self):
        logger.info(f"{self.user} requested master")
        if self.permissionlevel != PermissionLevel.ADMINISTRATOR:
            self.send_json({"type": "error", "command": "requestmaster", "msg": "Insufficient permissions for this command! "
                                                                                f"Permissionlevel: {self.permissionlevel.value}"})
            return
        self.master = self
        self.send_json({"type": "success", "command": "requestmaster", "msg": "Client set as master."})

    def ingame_event(self, content: dict):
        if self != self.master:
            self.send_json({"type": "error", "command": "event", "msg": "Only masters can submit events."})
            return
        eventtype = content.get('eventtype')

        self.sendall(content)

        model = objectmapping.get(eventtype, None)

        if model is None:
            return

        for key, val in content['data'].items():
            if type(val) != str:
                continue
            try:
                if re.match(r"\d{4}-\d{1,2}-\d{1,2}", val):
                    content['data'][key] = datetime.datetime.strptime(val, "%Y-%m-%d")
            except ValueError as e:
                print(e)

        obj = model.objects.create(**content['data'])

        obj.save()

    def sendall(self, content: dict, close=False):
        logger.debug(f"sending to all clients: {content}")
        for client in self.clients:
            try:
                client.send_json(content=content, close=close)
            except Exception as e:
                logger.exception(f"exception occured when sending to a client: {e}")
