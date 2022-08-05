from websocket import WebSocketApp, _logging
import json


class EventClientSocket(WebSocketApp):
    """
    handles the connection to the highscoresbot websocket api
    """
    def __init__(self, url):
        super().__init__(url,
                         on_open=self.on_open,
                         on_close=self.on_close,
                         on_message=self.on_message,
                         on_error=self.on_error)

    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)
        print("ERROR!!")

    def on_close(self, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self):
        self.send(data='{"type": "world"}')

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(*args)

            except Exception as e:
                _logging.error("error from callback {}: {}".format(callback, e))
                if self.on_error:
                    self.on_error(e)


if __name__ == "__main__":
    a = EventClientSocket("ws://127.0.0.1:8000/api/ingame_data/ws/gamedatareceiver/")
    a.run_forever()
