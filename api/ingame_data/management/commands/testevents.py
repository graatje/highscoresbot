import os
from abc import ABC

from django.core.management.base import BaseCommand

from websocket import WebSocketApp


class Command(BaseCommand, ABC):
    help = 'Connects to the django server and sends ingame events to that server.'

    def handle(self, *args, **options):
        self.stdout.write("starting websocket client")

        a = WebSocketApp(url="ws://127.0.0.1:8000/api/ingame_data/ws/gamedatareceiver/",
                         on_open=self._on_open,
                         on_close=lambda ws, status, close_msg: self.stdout.write("test over, websocket closed."),
                         )

        a.run_forever()

    def _on_open(self, ws):
        # login
        ws.send(f'{{"command": "login", "data": {{"username": "{os.environ.get("botusername")}", "password": "{os.environ.get("botpassword")}"}}}}')
        ws.send('{"command": "requestmaster"}')

        events = [
            # Altar Event
            '''
            {
                "data": {
                    "player": "Ash Ketchum",
                    "altartype": "Arceus",
                    "amount": "1"
                },
                "eventtype": "altar"
            }
            ''',

            # Altar Mounts Event
            '''
            {
                "data": {
                    "amountarceus": "2",
                    "maxarceus": "5",
                    "amountkyogre": "1",
                    "maxkyogre": "3",
                    "amountdiancie": "0",
                    "maxdiancie": "2"
                },
                "eventtype": "altaramounts"
            }
            ''',

            # Chest Event
            '''
            {
                "data": {
                    "player": "Misty",
                    "location": "Cerulean City",
                    "date": "2024-02-17"
                },
                "eventtype": "chest"
            }
            ''',

            # CWend Event
            '''
            {
                "data": {
                    "tier": 3,
                    "firstplace": "Brock",
                    "bpfirstplace": 500,
                    "secondplace": "May",
                    "bpsecondplace": 300,
                    "thirdplace": "Tracey",
                    "bpthirdplace": 150,
                    "bestplayer": "Ash Ketchum",
                    "bestplayerwins": 10,
                    "bestplayerlosses": 2
                },
                "eventtype": "cwend"
            }
            ''',

            # Elite4 Event
            '''
            {
                "data": {
                    "player": "Gary Oak",
                    "region": "Kanto",
                    "date": "2024-02-18"
                },
                "eventtype": "elite4"
            }
            ''',

            # Encounter Event
            '''
            {
                "data": {
                    "player": "Serena",
                    "level": 45,
                    "pokemon": "Fennekin",
                    "date": "2024-02-19"
                },
                "eventtype": "encounter"
            }
            ''',

            # Goldrush Event
            '''
            {
                "data": {
                    "location": "Goldenrod City"
                },
                "eventtype": "goldrush"
            }
            ''',

            # Honey Event
            '''
            {
                "data": {
                    "location": "Pallet Town"
                },
                "eventtype": "honey"
            }
            ''',

            # Itembomb Event
            '''
            {
                "data": {
                    "player": "Dawn",
                    "item": "Ultra Ball"
                },
                "eventtype": "itembomb"
            }
            ''',

            # Roll Event
            '''
            {
                "data": {
                    "player": "Clemont",
                    "level": 30,
                    "pokemon": "Magnemite",
                    "date": "2024-02-20"
                },
                "eventtype": "roll"
            }
            ''',

            # Swarm Event
            '''
            {
                "data": {
                    "pokemon1": "Pidgey",
                    "pokemon2": "Rattata",
                    "location": "Viridian Forest"
                },
                "eventtype": "swarm"
            }
            ''',

            # Tournament Event
            '''
            {
                "data": {
                    "tournament": "Little Cup",
                    "minstillstart": 5,
                    "prizes": "Rare Candy"
                },
                "eventtype": "tournament"
            }
            ''',

            # Worldboss Event
            '''
            {
                "data": {
                    "pokemon": "Rayquaza",
                    "location": "Sky Pillar",
                    "date": "2024-02-21"
                },
                "eventtype": "worldboss"
            }
            ''',

            # Worldbosstime Event
            '''
            {
                "data": {
                    "hours": "15",
                    "minutes": 30
                },
                "eventtype": "worldbosstime"
            }
            '''
        ]

        for event in events:
            data = '{"command": "event", "data":' + event + '}'
            data = data.replace("\n", "").replace(" ", "")
            self.stdout.write("sending: " + data)
            ws.send(data)

        ws.close()
