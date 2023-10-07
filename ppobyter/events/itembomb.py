import discord

from ppobyter.events.clanevent import ClanEvent


class IndividualBomb(ClanEvent):
    def __init__(self, player, item):
        self.item = item
        self.EVENTNAME = "itembomb"
        super(IndividualBomb, self).__init__(player)

    def determineRecipients(self):
        self._determinechannelrecipients()

    def makeMessage(self) -> discord.Embed:
        embed = discord.Embed(title=f"🎉Congratulations {self.player}!🎉",
                              description=f"{self.player} has received {self.item}",
                              colour=discord.Colour.magenta())
        return embed
