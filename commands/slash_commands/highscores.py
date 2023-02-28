from typing import Union

from api.eventconfigurations.models import Clanconfig
from discord import app_commands, Interaction
from discord.ext import commands
from api.highscores.models import HighscoreConfig
from commands.command_functionality import highscores
from commands.sendable import Sendable


async def highscorenameautocomplete(interaction: Interaction, current: str):
    suggestions = []
    async for highscoreconfig in HighscoreConfig.objects.filter(verbose_name__icontains=current).\
            order_by('verbose_name'):
        suggestions.append(app_commands.Choice(name=highscoreconfig.verbose_name,
                                               value=highscoreconfig.highscorename))
        if len(suggestions) == 25:
            break
    return suggestions


class Highscores(commands.Cog):
    def __init__(self, client):
        self.client: commands.bot.Bot = client
        self.databasepath = "highscores.db"

    highscoresgroup = app_commands.Group(name="highscores",
                                         description="all commands that have to do directly with all the highscores of pokemon planet.")

    @highscoresgroup.command(name="getplayer")
    async def getplayer(self, interaction: Interaction, username: str):
        await highscores.getplayer(Sendable(interaction), username)

    @highscoresgroup.command(name="getclan")
    async def getclan(self, interaction: Interaction, clanname: str = None):
        await highscores.getclan(Sendable(interaction), clanname)

    @highscoresgroup.command(name="top")
    @app_commands.autocomplete(highscorename=highscorenameautocomplete)
    async def top(self, interaction: Interaction, highscorename: str, clanname: str=None):
        sendable = Sendable(interaction)
        # if clanname is None:
        #     clanname = await self.getdefaultclanname(sendable, comment=False)
        await highscores.top(sendable, highscorename, clanname)

    @highscoresgroup.command(name="highscore")
    @app_commands.autocomplete(highscorename=highscorenameautocomplete)
    async def highscore(self, interaction: Interaction, highscorename: str, clanname: str=None):
        sendable = Sendable(interaction)
        await highscores.highscore(sendable, highscorename, clanname)

    @highscoresgroup.command(name="mapcontrol")
    async def mapcontrol(self, interaction: Interaction, clanname: str=None):
        sendable = Sendable(interaction)
        if clanname is None and ((clanname := await self.getdefaultclanname(sendable)) is None):
            clanname = ""
        await highscores.mapcontrol(sendable, clanname)

    async def getdefaultclanname(self, sendable: Sendable, comment=True) -> Union[str, None]:
        if sendable.guild is None:
            return

        clanconf = await Clanconfig.objects.aget(guild=sendable.guild.id)
        if clanconf is not None:
            return clanconf.clan.lower()
        if clanconf is None and comment:
            await sendable.send("Please register a default clanname or provide a clan in the command.")
        return None


async def setup(client: commands.Bot):
    await client.add_cog(Highscores(client))
