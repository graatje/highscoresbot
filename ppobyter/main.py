
import os
from typing import Any

import discord

#@todo check if nest_asyncio is still needed for websocket
import nest_asyncio  # this makes the discord client useable together with pyshark
from discord.ext import tasks

from ppobyter.eventscheduler import EventScheduler

nest_asyncio.apply()


class Main(discord.Client):
    def __init__(self, **options: Any):
        super().__init__(**options, intents=discord.Intents.default())
        self.__token = options["token"]
        self.running = False
        self.eventscheduler = EventScheduler(self)

    async def on_ready(self):
        await self.wait_until_ready()
        print("logged in as ", self.user)
        await self.handle_events.start()

    async def start(self):
        await super(Main, self).start(token=self.__token)

    @tasks.loop(seconds=4)
    async def handle_events(self):
        #print("running task.")
        while self.eventscheduler.eventAvailable():
            await self.eventscheduler.handleEvent()

    def add_event(self, event):
        self.eventscheduler.addEvent(event)



if __name__ == "__main__":
    Main(token=os.environ.get("token")).run()
