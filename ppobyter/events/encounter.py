import sqlite3
from .clanevent import ClanEvent
import datetime
import discord


class Encounter(ClanEvent):
    """
    This is an event that happens when someone encounters a pokemon.
    """
    def __init__(self, player: str, pokemon: str, level: str):
        """
        calls the init of the superclass and sets the pokemon and the level of it that pokemon was encountered.
        :param player: the player that encountered something.
        :param pokemon: The pokemon that was encountered.
        :param level: The level of the encountered pokemon.
        """
        # @todo mining encounter?
        self.pokemon = pokemon
        self.level = level
        self.EVENTNAME = "encounter"
        super(Encounter, self).__init__(player)

    def determineRecipients(self):
        """
        determines the channels the encounter must be sent to.
        :return:
        """
        self._determinechannelrecipients()

    def makeMessage(self) -> discord.embeds.Embed:
        """
        Makes the embed message to send to the channels.
        :return: discord embed
        """
        shiny = False
        if '[S]' in self.pokemon:
            shiny = True
        pokemonname = self.pokemon.replace("[S]", "")
        pokemonname = pokemonname.replace("[E]", "")

        if shiny:
            gif = r"http://play.pokemonshowdown.com/sprites/ani-shiny/{}.gif".format(pokemonname.lower())
        else:
            gif = r"http://play.pokemonshowdown.com/sprites/ani/{}.gif".format(pokemonname.lower())
        embed = discord.Embed(title="Congratulations {}!".format(self.player),
                              description=f"{self.player} has encountered a level {self.level} {self.pokemon}!",
                              color=0xFF5733)
        embed.set_thumbnail(url=gif)
        return embed
