import asyncio
import os
import threading
from json import JSONDecodeError
from websocket import WebSocketApp, _logging
import json

from ppobyter.eventmaker import EventMaker
from ppobyter.main import Main


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
        pass
        #self.send_json({"msg": "hello"})

    def on_message(self, message):
        try:
            self.on_json_message(json.loads(message))
        except JSONDecodeError:
            print("the server sent non-json data")
            print(message)
        # any other exceptions will get handled by on_error

    def on_json_message(self, message: dict):
        msgtype = message.get("type", None)
        if msgtype is None:
            print("messagetype was not provided.")
            return

        if msgtype == "ingamedata":
            event = EventMaker.makeEvent(eventname=message.get("eventtype", None),
                                         kwargs=message.get("data", {}))
            print(event)
            if event is not None:
                self.client.add_event(event)

    def send_json(self, message: dict):
        self.send(data=json.dumps(message))

    def on_error(self, error):
        self.send_json({"error": "an error has occured."})
        print(error)
        print("ERROR!!")

    def on_close(self, close_status_code, close_msg):
        print("### closed ###")

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(*args)

            except Exception as e:
                _logging.error("error from callback {}: {}".format(callback, e))
                self.on_error(e)


if __name__ == "__main__":
    a = EventClientSocket(url="ws://127.0.0.1:8000/api/ingame_data/ws/gamedatareceiver/",
                          token=os.environ.get("token"))
    a.run_forever()
