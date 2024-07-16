from typing import Union

import discord

import config
from .event import Event
import json


class Swarm(Event):
    """
    This event gets triggered when a swarm shows up.
    """
    def __init__(self, location: str, **kwargs):
        """
        This calls the superclass, sets the location, the first pokemon, and the second pokemon of the swarm.
        :param location: The location where the swarm showed up.
        :param kwargs: The pokemons that are part of the swarm + remaining swarm info.
        """
        self.location = location.lower()
        self.EVENTNAME = "swarm"
        super(Swarm, self).__init__()
        self.pokemon = {rarity: pokemons for rarity, pokemons in kwargs.items() if rarity in ["common", "uncommon", "rare", "veryRare", "extremelyRare", "legendary"]}

    def makeMessage(self) -> list:
        """
        Makes the message that gets sent to the recipients.
        :return: The message.
        """
        messages = [f"A swarm of Pokemon have invaded {self.location}!**\n"]
        for rarity, pokemons in self.pokemon.items():
            # Insert a space before every capital letter
            human_rarity_name = "".join([char if char.islower() else f" {char}" for char in rarity]).lower()
            messages[0] += f"**{human_rarity_name}**: " + ", ".join(pokemons) + "\n"

        location_embed = self._make_location_embed(self.location)
        if location_embed:
            messages.append(location_embed)

        return messages

    def determineRecipients(self, **kwargs):
        """
        Determines the recipients.
        """
       # self.__determinepmrecipients()
        self._determinechannelrecipients()

    # def __determinepmrecipients(self):
    #     """
    #     This determines the users that will receive a pm when this event shows up.
    #     They can either get a message for the location, or one of the pokemon, or a combination of both.
    #     """
    #     #@todo
    #     conn = sqlite3.connect(self.pathManager.getpath("eventconfigurations.db"))
    #     query = "SELECT playerid FROM pmswarm WHERE (location=? AND (pokemon=? OR pokemon=?) AND comparator='&') " \
    #             "OR ((location=? OR (pokemon=? OR pokemon=?)) AND comparator='|')"
    #     cur = conn.cursor()
    #     cur.execute(query, (self.location, self.pokemon1, self.pokemon2, self.location, self.pokemon1, self.pokemon2))
    #     playerids = [row[0] for row in cur.fetchall()]
    #     conn.close()
    #     # remove duplicates
    #     self._pmrecipients = list(set(playerids))

    def _make_location_embed(self, location_name) -> Union[discord.Embed, None]:
        with open(config.PPO_LOCATIONS_PATH, "r", encoding="utf-8") as file:
            locations_data = json.load(file)

        location = next(
            (location for location in locations_data["allLocationsData"] if location['name'].lower() == location_name.lower()), None)

        if not location:
            return None

        embed = discord.Embed(
            title=f'{location["name"]}',
            color=808080)

        imgurl = f"https://www.ppobuddy.com/locations/{location['region'].lower()}/{location['imageName'] if 'imageName' in location else location['_id']}.png"
        embed.set_image(url=imgurl)

        if "encounters" not in location:
            return None

        for category, pokemon_encounters in location["encounters"].items():  # example: land, list of pokemon
            embed.add_field(name=category.capitalize(), value=" ", inline=False)

            encounter_text_list = [
                f"{encounter_info['pokemonId'].capitalize()} <{config.RARITY_MAPPING.get(encounter_info['rarity'], 'Unknown Rarity')}>"
                for encounter_info in pokemon_encounters]

            locations_string = "\n".join(encounter_text_list)

            embed.add_field(name=" ", value=locations_string, inline=False)
        return embed
