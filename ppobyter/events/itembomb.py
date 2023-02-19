import discord

from ppobyter.events.clanevent import ClanEvent


class ItemBomb:
    def __init__(self, players, prizes):
        self.hitplayers = []
        try:
            user = players[0]
        except Exception as e:
            print(e)
            user = ""
        for index, player in enumerate(players):
            self.hitplayers.append(IndividualBomb(player, prizes[index], user))

    async def __call__(self, client):
        for hit in self.hitplayers:
            await hit(client)


class IndividualBomb(ClanEvent):
    def __init__(self, player, item, user):
        self.item = item
        self.EVENTNAME = "itembomb"
        self.user = user
        super(IndividualBomb, self).__init__(player)

    def determineRecipients(self):
        self._determinechannelrecipients()

    def makeMessage(self) -> discord.Embed:
        embed = discord.Embed(title=f"🎉Congratulations {self.player}!🎉",
                              description=f"{self.player} has received {self.item[1]} {self.item[0]} by {self.user}'s "
                                          f"item bomb!",
                              colour=discord.Colour.magenta())
        return embed
