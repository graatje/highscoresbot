import discord
from asgiref.sync import sync_to_async
from discord import app_commands, Interaction
from discord.ext import commands
from commands.command_functionality import eventconfigurations
from commands.sendable import Sendable
from api.ingame_data.models import Eventname
from api.eventconfigurations.models import Eventconfiguration, Playerconfig


async def permissionactionautocomplete(interaction: Interaction, current: str):
    return [app_commands.Choice(name="give role permissions", value="add"),
            app_commands.Choice(name="remove role permissions", value="remove"),
            app_commands.Choice(name="show role permissions", value="show")]


async def clanregistrationactionautocomplete(interaction: Interaction, current: str):
    return [app_commands.Choice(name="add to clan registrations", value="add"),
            app_commands.Choice(name="remove from clan registrations", value="remove"),
            app_commands.Choice(name="show clanregistrations", value="show")]


async def unregisterautocomplete(interaction: Interaction, current: str):
    result = []
    async for eventconfig in Eventconfiguration.objects.filter(channel__isnull=False, guild=interaction.guild.id):
        eventnamefunc = sync_to_async(eventconfig.get_eventname)
        eventname = await eventnamefunc()
        searchstr = f"{eventname}"
        if current in searchstr:
            result.append(app_commands.Choice(name=searchstr, value=eventconfig.id))
        if len(result) == 25:
            break
    return result


async def eventnameautocomplete(interaction: Interaction, current: str):
    eventnames = [app_commands.Choice(name=eventname.name, value=eventname.name)
                  async for eventname in Eventname.objects.all() if current in eventname.name]
    return eventnames[:25]


async def playerconfigactiontypeautocomplete(*args, **kwargs):
    return [app_commands.Choice(name="add player", value="add"),
            app_commands.Choice(name="remove player", value="remove"),
            app_commands.Choice(name="show players", value="show")]


async def playerconfigplayerautocomplete(interaction: Interaction, current: str):
    return [app_commands.Choice(name=config.player, value=config.player)
            async for config in Playerconfig.objects.filter(guild=interaction.guild.id) if current in config.player]


class Eventconfigurations(commands.Cog):
    """
    responsible for making sure the functionality gets the right parameters.
    """
    def __init__(self, client: commands.bot.Bot):
        self.client = client

    eventconfiggroup = app_commands.Group(name="eventconfig",
                                          description="configurate ingame events to be sent in certain channels")

    @eventconfiggroup.command(name="permissions")
    @app_commands.autocomplete(action=permissionactionautocomplete)
    async def permissions(self, interaction: Interaction, action: str, role: discord.Role = None):
        sendable = Sendable(interaction)
        if action != "show" and role is None:
            await sendable.send("please provide a role if you want to add or remove roles.")
            return
        if action == "add":
            await eventconfigurations.setperms(sendable, role)
        elif action == "remove":
            await eventconfigurations.removeperms(sendable, role)
        elif action == "show":
            await eventconfigurations.getperms(sendable)
        else:
            await sendable.send("Invalid action. Select an action from the autocomplete!")

    @eventconfiggroup.command(name="clanregistrations")
    @app_commands.autocomplete(action=clanregistrationactionautocomplete)
    async def clanregistrations(self, interaction: Interaction, action: str, clanname: str = None):
        sendable = Sendable(interaction)
        if clanname is None and action != "show":
            await sendable.send("Please provide a clanname if you want to add or remove clans.")
            return
        if action == "add":
            await eventconfigurations.registerclan(sendable, clanname)
        elif action == "remove":
            await eventconfigurations.unregisterclan(sendable, clanname)
        elif action == "show":
            await eventconfigurations.getclanregistrations(sendable)
        else:
            await sendable.send("Invalid action. Select an action from the autocomplete!")

    @eventconfiggroup.command(name="register")
    async def register(self, interaction: Interaction, channel: discord.TextChannel = None):
        sendable = Sendable(interaction)
        await eventconfigurations.register(sendable, channel)

    @eventconfiggroup.command(name="settime")
    @app_commands.autocomplete(eventname=eventnameautocomplete)
    async def settime(self, interaction: Interaction, eventname: str, time: int = None):
        sendable = Sendable(interaction)
        await eventconfigurations.settime(sendable, eventname, time)

    @eventconfiggroup.command(name="showregistrations")
    async def showregistrations(self, interaction: Interaction):
        sendable = Sendable(interaction)
        await eventconfigurations.showregistrations(sendable, self.client)

    @eventconfiggroup.command(name="unregister")
    @app_commands.autocomplete(id=unregisterautocomplete)
    async def unregister(self, interaction: Interaction, id: int):
        sendable = Sendable(interaction)
        await eventconfigurations.unregister(sendable, id)

    @eventconfiggroup.command(name="setpingrole")
    @app_commands.autocomplete(eventname=eventnameautocomplete)
    async def setpingrole(self, interaction: Interaction, eventname: str, pingrole: discord.Role = None):
        sendable = Sendable(interaction)
        await eventconfigurations.setpingrole(sendable, eventname, pingrole)

    @eventconfiggroup.command(name="playerconfig")
    @app_commands.autocomplete(actiontype=playerconfigactiontypeautocomplete,
                               player=playerconfigplayerautocomplete)
    async def playerconfig(self, interaction: Interaction, actiontype: str, player: str = None):
        sendable = Sendable(interaction)
        await eventconfigurations.playerconfig(sendable, actiontype, player)


async def setup(client):
    await client.add_cog(Eventconfigurations(client))
