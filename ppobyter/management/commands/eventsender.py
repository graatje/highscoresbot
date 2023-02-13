from abc import ABC
import os
from django.core.management.base import BaseCommand, CommandError

from ppobyter.wsclient import EventClientSocket

class Command(BaseCommand, ABC):
    help = 'Starts the part that listens for ingame data and sends them to discord.'

    def handle(self, *args, **options):
        print("hello world.")
        a = EventClientSocket(url="ws://127.0.0.1:8000/api/ingame_data/ws/gamedatareceiver/",
                              token=os.environ.get("discordtoken"))
        a.run_forever()
