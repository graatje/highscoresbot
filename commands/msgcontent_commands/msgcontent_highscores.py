import sqlite3
from typing import Union

import discord

from commands.interractions.discord_binder import DiscordBinder
from discord import User
from discord.ext import commands
from discord.ext.commands import Command

from commands.sendable import Sendable
from commands.utils.utils import tablify
from highscores import clanhighscores, RichestClans, BestClans
from highscores.highscore import Highscore
from commands.command_functionality.highscores import get_clancommands, get_top10cmds


class MsgContentHighscores(commands.Cog):
    def __init__(self, client):
        self.client: commands.bot.Bot = client
        self.databasepath = "highscores.db"
        self.makeClanCommands()
        self.makeTop10Commands()

    #user = get(bot.get_all_members(), id="1234")
    @commands.command(name="testcmd")
    async def testcmd(self, ctx):
        await ctx.send(f"{ctx.author.mention}")

    def makeClanCommands(self):
        for name, cmd in get_clancommands().items():
            self.client.add_command(commands.command(name=name)(cmd))

    def makeTop10Commands(self):
        for name, cmd in get_top10cmds().items():
            self.client.add_command(commands.command(name=name)(cmd))


async def setup(client: commands.Bot):
    await client.add_cog(MsgContentHighscores(client))
