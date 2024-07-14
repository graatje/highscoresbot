from abc import ABC
import os
from django.core.management.base import BaseCommand, CommandError
import time
from ppobyter.wsclient import EventClientSocket


class Command(BaseCommand, ABC):
    help = 'Starts the part that listens for ingame data and sends them to discord.'

    def handle(self, *args, **options):
        print("hello world.")

        while True:
            try:
                a = EventClientSocket(url=f"ws://{os.environ.get('app_domain', 'localhost')}:{os.environ.get('app_port', 80)}/api/ingame_data/ws/gamedatareceiver/",
                                      token=os.environ.get("discordtoken"),
                                      username=os.environ.get("botusername"),
                                      password=os.environ.get("botpassword")
                                      )
                a.run_forever()
            except Exception as e:
                print("EXCEPTION OCCURRED: " + str(e))
            time.sleep(10)
