from __future__ import annotations

import datetime
import re
from typing import List, Union

from django.contrib.auth import authenticate
from jsonschema.exceptions import ValidationError

import log
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from api.enums import PermissionLevel
from api.highscoresbot_api.models import User
from api.ingame_data.consumers.validators.validators import Validators
from api.ingame_data.objectmapping import objectmapping
logger = log.Logger()


class GameDataConsumer(JsonWebsocketConsumer):
    clients: List[GameDataConsumer] = []
    configs = {
        "master": None
    }
    commandResponses = {}

    def __init__(self, *args, **kwargs):
        super(GameDataConsumer, self).__init__(args=args, kwargs=kwargs)
        self.user: Union[User, AnonymousUser] = AnonymousUser()
        self.permissionlevel = PermissionLevel.UNAUTHORIZED

    def connect(self):
        super().connect()
        self.clients.append(self)
        self.user: User = self.scope["user"]  # is actually UserLazyObject but has same attributes as user
        logger.info(f"{self.user} connected.")

    def receive_json(self, content, **kwargs):
        try:
            Validators.validateJson(content.get('command', None), content)
        except ValidationError as e:
            self.send_json(
                {
                    'command': content.get('command', None),
                    'success': False,
                    'message': e.message
                }
            )
            return
        actiontype = content.get('command')
        print(content)
        data = content.get('data', {})

        if actiontype == "login":
            self.login(data.get("username"), data.get("password"))
        elif actiontype == "logout":
            self.logout()
        elif actiontype == "disconnect":
            if self == self.configs["master"]:
                self.sendall(
                    {
                        "command": "disconnect",
                        "success": True,
                        "message": "Master disconnected."
                     }
                )
        elif actiontype == "event":
            self.ingame_event(content)
        elif actiontype == "requestmaster":
            self.requestMaster()
        elif actiontype == "registercommand":
            if self.permissionlevel == self.permissionlevel.UNAUTHORIZED:
                self.send_json(
                    {
                        "command": "registercommand",
                        "success": False,
                        "message": "Insufficient permissions for this command!"
                    }
                )
                return
            elif self.user.prefix is None:
                self.send_json(
                    {
                        "command": "registercommand",
                        "success": False,
                        "message": "You have no prefix set! Please contact kevin123456 on discord."
                    }
                )
                return
            content["data"]["prefix"] = self.user.prefix
            content["data"]["user_id"] = self.user.id
            self.configs["master"].send_json(content)

            content["success"] = True
            self.send_json(content)
        elif actiontype == "command":
            if self != self.configs["master"]:
                self.send_json(
                    {
                        "command": "commandresponse",
                        "success": False,
                        "message": "Only master can submit commands."
                    }
                )
                return
            # Fetch the user
            user = User.objects.get(id=data.get("user_id"))
            if not user:
                return

            if not (clients := [client for client in self.clients if client.user == user]):
                return
            client = clients[0]

            self.commandResponses[data.get("uid")] = client

            # send the command to the client
            client.send_json(content)
        elif actiontype == "commandresponse":
            if self != self.commandResponses.get(data.get("uid"), None):
                self.send_json(
                    {
                        "command": "commandresponse",
                        "success": False,
                        "message": "This command response is not for you or does not exist.",
                        "data": {
                            "uid": data.get("uid")
                        },
                    }
                )
                return
            self.configs["master"].send_json(content)

    def login(self, username, password):
        user = authenticate(username=username, password=password)

        if user is not None:
            logger.info(f"{user} logged in.")
            self.user = user
            if self.user.is_superuser:
                self.permissionlevel = PermissionLevel.ADMINISTRATOR
            else:
                self.permissionlevel = PermissionLevel.LOGGED_IN
            self.send_json(
                {
                    "command": "login",
                    "success": True,
                    "message": "login successfull",
                    "data": {
                        "permissionlevel": self.permissionlevel.value
                    }
                }
            )
        else:
            self.send_json(
                {
                    "command": "login",
                    "success": False,
                    "message": "Invalid credentials"
                }
            )

    def logout(self):
        logger.info(f"{self.user} logged out")
        self.user = AnonymousUser()
        self.permissionlevel = PermissionLevel.UNAUTHORIZED
        self.send_json(
            {
                "command": "logout",
                "success": True,
                "message": "Successfully logged out"
            }
        )

    def requestMaster(self):
        logger.info(f"{self.user} requested master")
        if self.permissionlevel != PermissionLevel.ADMINISTRATOR:
            self.send_json(
                {
                    "command": "requestmaster",
                    "success": False,
                    "message": "Insufficient permissions for this command! " + f"Permissionlevel: {self.permissionlevel.value}"
                }
            )
            return
        self.configs["master"] = self
        self.send_json(
            {
                "command": "requestmaster",
                "success": True,
                "message": "Client set as master."
            }
        )

    def ingame_event(self, content: dict):
        if self != self.configs["master"]:
            self.send_json(
                {
                    "command": "event",
                    "success": False,
                    "message": "Only masters can submit events."
                }
            )
            return
        data = content.get('data', {})
        eventtype = data.get('eventtype')

        # Data is already validated before this method is called so type is success.
        content["success"] = True

        self.sendall(content)

        model = objectmapping.get(eventtype, None)

        if model is None:
            return

        for key, val in content['data']['data'].items():
            if type(val) != str:
                continue
            try:
                if re.match(r"\d{4}-\d{1,2}-\d{1,2}", val):
                    content['data']['data'][key] = datetime.datetime.strptime(val, "%Y-%m-%d")
            except ValueError as e:
                print(e)

        obj = model.objects.create(**data['data'])

        obj.save()

    def sendall(self, content: dict, close=False):
        logger.debug(f"sending to all clients: {content}")
        for client in self.clients:
            try:
                client.send_json(content=content, close=close)
            except Exception as e:
                logger.exception(f"exception occurred when sending to a client: {e}")
