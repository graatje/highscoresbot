import sqlite3
from typing import Union

from asgiref.sync import sync_to_async
from discord import Interaction
from discord.ui import TextInput
from commands.interractions.pmconfig.pmconfig import PmConfigModel
from commands.interractions.pmconfig.pmgoldrush import PmGoldrush
from commands.interractions.pmconfig.pmhoney import PmHoney
from commands.interractions.pmconfig.removepmconfig import RemovePmConfig
from commands.interractions.selectsview import SelectsView
from commands.sendable import Sendable
from commands.utils.utils import getgoldrushlocations, gethoneylocations, getswarmpokemons, getswarmlocations
from db.config.models import Eventname
from db.eventconfigurations.models import PmConfig


async def getEventObject(eventname: str) -> Union[Eventname, None]:
    try:
        return await (sync_to_async(Eventname.objects.get))(name__iexact=eventname)
    except Eventname.DoesNotExist:
        return None


async def pmconfig(interaction: Interaction, eventname: str):
    eventobj = await getEventObject(eventname)
    if eventobj is None:
        await interaction.response.send_message("Not a valid eventname! Select an eventname from the autocomplete!")
        return
    textinputs = []
    for key, value in eventobj.fields.items():
        textinputs.append(TextInput(label=value,
                                    required=False,
                                    custom_id=key))

    await interaction.response.send_modal(PmConfigModel(textinputs, event=eventobj))
#    await interaction.response.pong()


async def removepmconfig(sendable: Sendable, id):
    """
    Starts user interaction to remove pm configuration of certain events.
    Fails if the time limit of 30 seconds to respond has expired.
    Asks for either a list of id's or a single id, and deletes those. Note that the id's are just list indexes, it
    gets the values at those list indexes to delete the configurations.
    :param ctx: discord context.
    """
    try:
        obj: PmConfig = await PmConfig.objects.aget(user=sendable.user.id, id=id)
        await (sync_to_async(obj.delete))()
        await sendable.send("configuration deleted!")
    except PmConfig.DoesNotExist:
        await sendable.send("requested pmconfig does not exist, please select an option from the autocomplete!")
