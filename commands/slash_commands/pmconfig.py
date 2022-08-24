from asgiref.sync import sync_to_async
from discord import app_commands, Interaction
from discord.ext import commands
from commands.command_functionality import pmconfig
from commands.interractions.pmconfig.pmconfig import PmConfigModel
from commands.interractions.pmconfig.pmswarm import swarmpokemonautocomplete, swarmlocationautocomplete
from commands.interractions.pmconfig.pmtournament import tournamenttypeautocomplete, tournamentprizeautocomplete
from commands.interractions.pmconfig.pmworldboss import worldbosspokemonautocomplete, worldbosslocationautocomplete
from commands.sendable import Sendable
from db.config.models import Eventname
from db.eventconfigurations.models import PmConfig


async def eventnameautocomplete(interaction: Interaction, current: str):
    eventnames = [app_commands.Choice(name=eventname.name, value=eventname.name)
                  async for eventname in Eventname.objects.all() if current in eventname.name]
    return eventnames[:25]


async def pmconfigautocomplete(interaction: Interaction, current: str):
    result = {}
    obj: PmConfig
    async for obj in PmConfig.objects.filter(user=interaction.user.id):
        event: Eventname = await (sync_to_async(obj.fetch_event))()
        name = f"{event.name} event, "
        name += ", ".join([event.fields.get(field, "") + ": " + obj.data.get(field, "")
                           for field in obj.data])
        if current in name:
            result[obj.id] = {"name": name, "fields": len(obj.data)}

    # less fields have more priority since less fields mean less specific events,
    # thus more eventannouncements for that event
    autocompletion = []
    for key, value in sorted(result.items(), key=lambda item: item[1]["fields"]):
        autocompletion.append(app_commands.Choice(name=value["name"], value=key))
        if len(autocompletion) == 25:
            break
    return autocompletion


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
    @app_commands.autocomplete(id=pmconfigautocomplete)
    async def removepmconfig(self, interaction: Interaction, id: int):
        sendable = Sendable(interaction)
        await pmconfig.removepmconfig(sendable, id)


async def setup(client):
    await client.add_cog(Pmconfig(client))
