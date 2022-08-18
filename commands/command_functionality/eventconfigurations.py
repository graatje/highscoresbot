import discord
from asgiref.sync import sync_to_async
from discord import NotFound, Forbidden
from django.db import IntegrityError

from commands.interractions.eventconfig.register import Register
from commands.interractions.resultmessageshower import ResultmessageShower
from commands.interractions.selectsview import SelectsView
from commands.sendable import Sendable
from commands.utils.utils import haspermissions, tablify
from discord.utils import MISSING
from typing import Union

from db.config.models import Eventname
from db.eventconfigurations.models import EventconfigPermissions, Eventconfiguration, Clanconfig, Playerconfig


async def fetch_eventconfig(guildid: int, event: Eventname) -> Eventconfiguration:
    """
    fetches an event. if it does not exist it creates a basic one (just guildid and event)
    :param guildid:
    :param event: Eventname object.
    :return: The existing Eventconfiguration or a new one.
    """
    try:
        return await (sync_to_async(Eventconfiguration.objects.get))(guild=guildid, eventname=event)
    except Eventconfiguration.DoesNotExist:
        createfunc = sync_to_async(Eventconfiguration.objects.create)
        return await createfunc(guild=guildid, eventname=event)


async def getEventObject(eventname) -> Union[Eventname, None]:
    try:
        return await (sync_to_async(Eventname.objects.get))(name__iexact=eventname)
    except Eventname.DoesNotExist:
        return None


async def setperms(sendable: Sendable, role: discord.Role):
    """
    This command gives permission to the specified role to adjust eventconfigurations for this server.
    Only useable by administrators of the server.
    :param sendable: Sendable object.
    :param role: the role id or the role mention. Union[int, str]
    """
    if not sendable.user.guild_permissions.administrator:
        await sendable.send("only administrators can use this command!")
        return

    func = sync_to_async(EventconfigPermissions.objects.create)
    try:
        await func(guild=sendable.guild.id, role=role.id)
        await sendable.send("role successfully given permissions.")
    except IntegrityError:
        await sendable.send("role already had permissions.")
    except Exception as e:
        await sendable.send("unknown error.")
        raise e


async def removeperms(sendable: Sendable, role: discord.Role):
    """
    Removes the permissions of a role to adjust eventconfigurations for this server.
    Only useable by administrators of the server.
    :param sendable: Sendable object.
    :param role: the role id or the role mention. Union[int, str]
    """
    if not sendable.user.guild_permissions.administrator:
        await sendable.send("only administrators can use this command!")
        return
    func = sync_to_async(EventconfigPermissions.objects.get)
    try:
        obj = await func(guild=sendable.guild.id, role=role.id)
        deletefunc = sync_to_async(obj.delete)
        await deletefunc()
        await sendable.send("Role successfully removed from permissions.")
    except EventconfigPermissions.DoesNotExist:
        await sendable.send("that role had no permissions.")
    except Exception as e:
        await sendable.send("unknown exception occured.")
        raise e


async def getperms(sendable: Sendable):
    """
    Gets the roles that have permission to adjust eventconfigurations.
    :param sendable: Sendable object.
    """
    roleids = [config.role async for config in EventconfigPermissions.objects.filter(guild=sendable.guild.id)]
    if not roleids:
        await sendable.send("no permissions set.")
        return
    message = "```\n"
    for roleid in roleids:
        role = sendable.guild.get_role(roleid)
        if role is not None:
            message += str(role) + "\n"
    message += "\n```"
    await sendable.send(message)


async def register(sendable: Sendable, channel: discord.TextChannel = None):
    """
    Registers an event at the specified channel. If the channel is not specified the channel is the channel the
    command is used from.
    :param sendable: Sendable object.
    :param channel: The channel to send the event to. Default channel where command was used.
    """
    print("WARNING: PERMISSIONS BYPASSED")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    chan = channel if channel is not None else sendable.channel
    eventnames = [eventname.name async for eventname in Eventname.objects.all().order_by('name')]
    view = SelectsView(sendable, eventnames, lambda options: Register(sendable, options, chan))
    await sendable.send(f"Select events you want a message for in {chan.mention}", view=view)


async def settime(sendable: Sendable, eventname: str, time: int = None):
    """
    Sets the time in minutes the event should stay in the channel. Default removes the time, so the message won't
    get deleted anymore.
    :param sendable: Sendable object
    :param eventname: The name of the event
    :param time: the time the message of the event should stay in the channel. Default None.
    """
    print("WARNING: PERMISSIONS BYPASSED")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    eventname = eventname.lower()
    try:
        if time is not None:
            time = int(time)
    except ValueError:
        await sendable.send("please provide a valid time!")
        return
    # if not await __eventnamecheck(sendable, eventname):
    #     return
    event = await getEventObject(eventname)

    eventconfig = await fetch_eventconfig(event=event, guildid=sendable.guild.id)
    eventconfig.time_in_channel = time
    savefunc = sync_to_async(eventconfig.save)
    await savefunc()
    if time is not None:
        await sendable.send(f"messages for the {eventname} event will be removed after {time} minutes. ")
    else:
        await sendable.send(f"messages for the {eventname} event won't be removed after a certain time anymore.")


async def getclanregistrations(sendable: Sendable):
    clans = [clanconfig.clan async for clanconfig in Clanconfig.objects.filter(guild=sendable.guild.id)]
    if 'all' in [clan.lower() for clan in clans]:
        await sendable.send("all clans have been registered, since you have 'all' registered.")
    else:
        await sendable.send("The following clans have been registered for this server:\n" + "\n".join(clans))


async def showregistrations(sendable: Sendable, client: discord.Client):
    eventconfigs = [eventconfig async for eventconfig in Eventconfiguration.objects.filter(guild=sendable.guild.id)]
    result = []
    for eventconfig in eventconfigs:
        # getting channel name
        if eventconfig.channel is not None:
            try:
                channel = await client.fetch_channel(eventconfig.channel)
                channel = str(channel)
            except NotFound:
                channel = "not found"
            except Forbidden:
                channel = "no permissions"
            except Exception as e:
                print(e)
                channel = "unknown"
        else:
            channel = "not available"

        # getting rolename
        if eventconfig.pingrole is not None:
            try:
                role = str(sendable.guild.get_role(eventconfig.pingrole))
            except Exception as e:
                print("fetching role failed.")
                print(e)
                role = "failed to fetch role"
        else:
            role = "not available"

        eventnamefunc = sync_to_async(eventconfig.get_eventname)
        eventname = await eventnamefunc()
        result.append((eventname, channel, role, eventconfig.time_in_channel))
    messages = tablify(["eventname", "channel", "pingrole", "alivetime"], result)
    view = MISSING
    if len(messages) > 1:
        view = ResultmessageShower(messages, interaction=sendable)
    await sendable.send(messages[0], view=view)


async def unregisterclan(sendable: Sendable, clanname: str):
    """
    removes a clan from clanregistrations. So elite4/encounters/chests won't be announced in the server if a player
    with that clan triggers that event.
    :param sendable: Sendable object
    :param clanname: The clanname
    """
    print("WARNING: BYPASSING PERMISSIONS!")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    clannames = [clanconfig.clan async for clanconfig in Clanconfig.objects.filter(guild=sendable.guild.id)]
    if clanname == 'all' and 'all' not in [clan.lower() for clan in clannames]:
        deletefunc = sync_to_async(Clanconfig.objects.filter(guild=sendable.guild.id).delete)
        await deletefunc()
    elif clanname == "all":
        objfunc = sync_to_async(Clanconfig.objects.get)
        obj = await objfunc(guild=sendable.guild.id, clan='all')
        deletefunc = sync_to_async(obj.delete)
    else:
        objfunc = sync_to_async(Clanconfig.objects.get)
        obj = await objfunc(guild=sendable.guild.id, clan__iexact=clanname)
        deletefunc = sync_to_async(obj.delete)
    await deletefunc()
    clannames = [clanconfig.clan async for clanconfig in Clanconfig.objects.filter(guild=sendable.guild.id)]
    await sendable.send(f"configuration for {clanname} removed!\n"
                                            "remaining clans: ```\n" + "\n".join(clannames) + "```")


async def registerclan(sendable: Sendable, clanname: str):
    """
    registers a clan to the server, then if the event(s) are registered, chests, encounters and elite 4 (among
    others) will be sent to the server if the member who caused the event is part of the clan that is registered.
    :param sendable: Sendable object
    :param clanname: The name of the clan.
    """
    print("WARNING: BYPASSING PERMISSIONS!")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.response.send_message("insufficient permissions to use this command!")
    #     return
    try:
        func = sync_to_async(Clanconfig.objects.create)
        await func(guild=sendable.guild.id, clan=clanname)
        await sendable.send(f"successfully registered {clanname}")
    except IntegrityError:
        await sendable.send("guild already registered.")


async def unregister(sendable: Sendable, id: int):
    """
    Sets the channel of the provided event to null, that way the provided event will not be sent anymore to that
    server.
    :param sendable: Sendable object
    :param id: the id of the event
    """
    print("WARNING: BYPASSING AUTH!")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not \
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    eventconfigfunc = sync_to_async(Eventconfiguration.objects.get)
    try:
        eventconfig: Union[Eventconfiguration, None] = await eventconfigfunc(id=id)
    except Eventconfiguration.DoesNotExist:
        eventconfig = None
    if eventconfig is None or eventconfig.guild != sendable.guild.id:
        await sendable.send("unauthorized or event not found. please select something in the autocomplete!")
        return
    deletefunc = sync_to_async(eventconfig.delete)
    await deletefunc()
    await sendable.send("event successfully removed!")


async def setpingrole(sendable: Sendable, eventname: str, pingrole: discord.Role):
    """
    Adds a ping of the provided role to the event message.
    :param sendable: Sendable object
    :param eventname: The name of the event.
    :param pingrole: The role id or the role mention.
    """
    print("WARNING: BYPASSING AUTH")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    event = await getEventObject(eventname)
    if event is None:
        await sendable.send("invalid eventname.")
        return
    eventconfig = await fetch_eventconfig(sendable.guild.id, event)
    eventconfig.pingrole = pingrole.id
    savefunc = sync_to_async(eventconfig.save)
    await savefunc()
    await sendable.send("pingrole set!")


async def removeping(sendable: Sendable, eventname: str):
    """
    Removes the ping of the provided event for the guild it was used in.
    :param sendable: Sendable object
    :param eventname: the name of the event.
    """
    print("WARNING: AUTH BYPASSED!")
    # if not haspermissions([role.id for role in sendable.user.roles], sendable.guild.id) and not\
    #         sendable.user.guild_permissions.administrator:
    #     await sendable.send("insufficient permissions to use this command!")
    #     return
    event = await getEventObject(eventname)
    eventconfig = await fetch_eventconfig(guildid=sendable.guild.id, event=event)
    eventconfig.pingrole = None
    await (sync_to_async(eventconfig.save))()
    await sendable.send("pingrole removed if it was set!")


async def playerconfig(sendable: Sendable, actiontype: str, player: str=None):
    """
    add players, remove players and show players that act as if a player is in a clan.
    :param sendable: Sendable object
    :param actiontype: 'add', 'remove', or 'show'
    :param player: can only be None when actiontype is 'show'.
    """
    if actiontype in ["add", "remove"] and player is None:
        await sendable.send(f"please specify a player to {actiontype}.")
        return

    if actiontype == 'add':
        try:
            await (sync_to_async(Playerconfig.objects.create))(guild=sendable.guild.id, player=player)
            await sendable.send(f"{player} added to playerconfig!")
        except IntegrityError:
            await sendable.send("player already exists in playerconfig.")
    elif actiontype == "remove":
        try:
            obj = await (sync_to_async(Playerconfig.objects.get))(guild=sendable.guild.id, player=player)
            await (sync_to_async(obj.delete))()
            await sendable.send(f"{player} removed from playerconfig.")
        except Playerconfig.DoesNotExist:
            await sendable.send(f"{player} was not configured so could not be deleted.")
    elif actiontype == "show":
        await sendable.send("The following players have been registered for playerconfig:\n```" +
                            "\n".join([config.player
                                       async for config in Playerconfig.objects.filter(guild=sendable.guild.id)]) +
                            "```")
    else:
        await sendable.send("invalid actiontype. Please select an actiontype from the autocomplete!")
