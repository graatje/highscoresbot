from discord import app_commands, Interaction
from discord.ext import commands
from commands.command_functionality import pmconfig
from commands.interractions.pmconfig.pmconfig import PmConfigModel
from commands.interractions.pmconfig.pmswarm import swarmpokemonautocomplete, swarmlocationautocomplete
from commands.interractions.pmconfig.pmtournament import tournamenttypeautocomplete, tournamentprizeautocomplete
from commands.interractions.pmconfig.pmworldboss import worldbosspokemonautocomplete, worldbosslocationautocomplete
from commands.sendable import Sendable
from db.config.models import Eventname


async def eventnameautocomplete(interaction: Interaction, current: str):
    eventnames = [app_commands.Choice(name=eventname.name, value=eventname.name)
                  async for eventname in Eventname.objects.all() if current in eventname.name]
    return eventnames[:25]


class Pmconfig(commands.Cog):
    """
    This class contains commands for the configuration of events in pm's.
    """
    def __init__(self, client):
        self.client = client
        self.databasepath = "./eventconfigurations.db"

    pmconfiggroup = app_commands.Group(name="pmconfig", description="deals with sending ingame events to channels")

    @pmconfiggroup.command(name="pmconfig")
    @app_commands.autocomplete(eventname=eventnameautocomplete)
    async def pmconfig(self, interaction: Interaction, eventname: str):
        await pmconfig.pmconfig(interaction, eventname)

    @pmconfiggroup.command(name="removepmconfig")
    async def removepmconfig(self, interaction: Interaction):
        sendable = Sendable(interaction)
        await pmconfig.removepmconfig(sendable)


async def setup(client):
    await client.add_cog(Pmconfig(client))
