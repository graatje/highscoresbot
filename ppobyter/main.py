import os
from typing import Any

import discord

#@todo check if nest_asyncio is still needed for websocket
import nest_asyncio  # this makes the discord client useable together with pyshark


nest_asyncio.apply()


class Main(discord.Client):
    def __init__(self, **options: Any):
        super().__init__(**options)
        self.__token = options["token"]
        self.running = False

    async def on_ready(self):
        await self.wait_until_ready()
        print("ready.")

    def run(self):
        super(Main, self).run(token=self.__token)


if __name__ == "__main__":
    Main(token=os.environ.get("token")).run()
