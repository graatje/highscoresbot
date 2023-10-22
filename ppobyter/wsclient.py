import asyncio
import os
import threading
from json import JSONDecodeError

from dotenv import load_dotenv
from websocket import WebSocketApp
import json

from ppobyter.eventmaker import EventMaker
from ppobyter.events.disconnect import Disconnect
from ppobyter.ingame_commands import ingame_data
from ppobyter.ingame_commands.framework.ingamecommand import IngameCommand
from ppobyter.main import Main
import log
load_dotenv()
logger = log.Logger()


class EventClientSocket(WebSocketApp):
    """
    handles the connection to the highscoresbot websocket api
    """
    def __init__(self, url, token, username, password):
        self.__username = username
        self.__password = password
        super().__init__(url,
                         on_open=self.on_open,
                         on_close=self.on_close,
                         on_message=self.on_message,
                         on_error=self.on_error)
        self.client = Main(token=token)
        t = threading.Thread(target=lambda: asyncio.run(self.client.start()))
        t.start()
        self.commands = {}

    def on_open(self):
        logger.info("connected to server.")
        self.login(self.__username, self.__password)

        self.register_commands()

    def login(self, username, password):
        self.send_json({"command": "login",
                        "data": {"username": username,
                                 "password": password}})

    def on_message(self, message):
        try:
            self.on_json_message(json.loads(message))
        except JSONDecodeError:
            logger.warning(f"the server sent non-json data, {message}")
        # any other exceptions will get handled by on_error

    def on_json_message(self, message: dict):
        command = message.get("command", None)
        if command is None:
            logger.debug("message type not provided")
            return

        if command == "event":
            logger.debug("command type is ingame data")
            data = message.get("data", {})
            event = EventMaker.makeEvent(eventname=data.get("eventtype", None),
                                         **data.get("data", {}))

            if event is not None:
                logger.debug(f"following event made: {event}")
                self.client.add_event(event)
        elif command == "disconnect":
            logger.debug("client disconnected from gameserver.")
            self.client.add_event(Disconnect())
        elif command == "command":
            messages = self.commands.get(message["data"]["command"]).execute(**message["data"]["arguments"])
            resp = {
                "command": "commandresponse",
                "data": {
                    "uid": message["data"]["uid"],
                    "messages": messages
                },
            }
            self.send_json(resp)
            print("command working.")
        else:
            logger.warning("unknown command: " + str(message))

    def send_json(self, message: dict):
        logger.debug(f"sent {message}")
        self.send(data=json.dumps(message))

    def register_commands(self):
        ingame_data.register_commands(self)

    def register_command(self, command: IngameCommand):
        self.commands[command.name] = command
        self.send_json({
            "command": "registercommand",
            "data": command.to_json()
        })

    def on_error(self, error):
        logger.exception(f"an exception has occured: {str(error)}")

    def on_close(self, close_status_code, close_msg):
        logger.info(f"websocket closed with status code: {close_status_code} and message: {close_msg}.")

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(*args)

            except Exception as e:
                logger.error("error from callback {}: {}".format(callback, e))
                self.on_error(e)


if __name__ == "__main__":
    a = EventClientSocket(url="ws://127.0.0.1:8000/api/ingame_data/ws/gamedatareceiver/",
                          token=os.environ.get("discordtoken"))
    a.run_forever()
