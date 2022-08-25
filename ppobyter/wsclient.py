import asyncio
import os
import threading
from json import JSONDecodeError

from dotenv import load_dotenv
from websocket import WebSocketApp
import json

from ppobyter.eventmaker import EventMaker
from ppobyter.main import Main
import log
load_dotenv()
logger = log.Logger()


class EventClientSocket(WebSocketApp):
    """
    handles the connection to the highscoresbot websocket api
    """
    def __init__(self, url, token):
        super().__init__(url,
                         on_open=self.on_open,
                         on_close=self.on_close,
                         on_message=self.on_message,
                         on_error=self.on_error)
        self.client = Main(token=token)
        t = threading.Thread(target=lambda: asyncio.run(self.client.start()))
        t.start()

    def on_open(self):
        logger.info("connected to server.")

    def on_message(self, message):
        try:
            self.on_json_message(json.loads(message))
        except JSONDecodeError:
            logger.warning(f"the server sent non-json data, {message}")
        # any other exceptions will get handled by on_error

    def on_json_message(self, message: dict):
        msgtype = message.get("type", None)
        if msgtype is None:
            logger.debug("message type not provided")
            return

        if msgtype == "ingamedata":
            logger.debug("message type is ingame data")
            event = EventMaker.makeEvent(eventname=message.get("eventtype", None),
                                         kwargs=message.get("data", {}))

            if event is not None:
                logger.debug(f"following event made: {event}")
                self.client.add_event(event)

    def send_json(self, message: dict):
        logger.debug(f"sent {message}")
        self.send(data=json.dumps(message))

    def on_error(self, error):
        self.send_json({"error": "an error has occured."})
        logger.exception(f"an exception has occured: {str(error)}")

    def on_close(self, close_status_code, close_msg):
        logger.info(f"websocket closed with status code: {close_status_code}   and message: {close_msg}.")

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
