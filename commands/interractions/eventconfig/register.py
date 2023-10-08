from typing import List
import discord
from django.db import IntegrityError

from api.ingame_data.models import Eventname
from api.eventconfigurations.models import Eventconfiguration
from asgiref.sync import sync_to_async
from commands.interractions.selectsutility import SelectsUtility


class Register(SelectsUtility):
    def __init__(self, interaction, options: List[str], channel: discord.channel.TextChannel):
        super().__init__(interaction=interaction, options=options, max_selectable=len(options),
                         placeholder="select events to register for:")
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        for event in self.values:

            func = sync_to_async(Eventname.objects.get)
            eventobj = await func(name=event)
            try:
                eventconfigfunc = sync_to_async(Eventconfiguration.objects.get)
                eventconfig: Eventconfiguration = await eventconfigfunc(eventname=eventobj, guild=self.channel.guild.id)
                eventconfig.channel = self.channel.id
                await (sync_to_async(eventconfig.save))()
            except Eventconfiguration.DoesNotExist:
                createfunc = sync_to_async(Eventconfiguration.objects.create)
                await createfunc(eventname=eventobj, guild=self.channel.guild.id, channel=self.channel.id)

            await self.channel.send(
                    f"This channel has been properly configured for sending the {event} event "
                    f"{self.interaction.user.mention}!")
            if not interaction.response.is_done():
                await interaction.response.send_message("success!")
