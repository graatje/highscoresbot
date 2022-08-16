from abc import ABC
import discord
from asgiref.sync import sync_to_async
from discord import Interaction

from commands.interractions.browseselection import BrowseSelection
from db.highscores.models import HighscoreConfig, Highscore
from utils.tablify_dict import tablify_dict


class HighscoreCommand(BrowseSelection, ABC):
    def __init__(self, interaction: Interaction, highscorename, clanname: str=None):
        """
        creates a selectsutility for the highscore command.
        :param ctx:
        :param highscores: the options. max 25.
        """
        super(HighscoreCommand, self).__init__(pagesamount=float('inf'),
                                               interaction=interaction, ownerOnly=True)
        self.highscoreName = highscorename
        self.highscoreConfig = None
        self.clanname = clanname
        self.PAGE_SIZE = 20

    async def init(self):
        func = sync_to_async(HighscoreConfig.objects.get)
        self.highscoreConfig = await func(highscorename=self.highscoreName)
        if self.clanname is not None:
            qs = Highscore.objects.filter(highscore=self.highscoreConfig,
                                          data__clan__iexact=self.clanname).order_by("rank")
            tablified = tablify_dict([value.to_json() async for value in qs],
                                     order=["rank", "username", "clan"],
                                     verbose_names=dict(self.highscoreConfig.fieldmapping))
            self.maxpage = len(tablified)
        else:
            self.maxpage = self.highscoreConfig.pagesamount * 100 / self.PAGE_SIZE

    async def _sendPage(self, interaction: discord.Interaction):

        await interaction.response.edit_message(content=await self.getPage(), view=self)

    async def getPage(self) -> str:
        if self.clanname is None:
            qs = Highscore.objects.filter(highscore=self.highscoreConfig,
                                          rank__range=((self.currentpage - 1) * self.PAGE_SIZE, self.currentpage * self.PAGE_SIZE)).order_by("rank")
        else:
            qs = Highscore.objects.filter(highscore=self.highscoreConfig,
                                          data__clan__iexact=self.clanname).order_by("rank")
        tablified = tablify_dict([value.to_json() async for value in qs],
                            order=["rank", "username", "clan"],
                            verbose_names=dict(self.highscoreConfig.fieldmapping))
        if self.clanname is not None:
            return tablified[self.currentpage-1]
        return tablified[0]
