import datetime
import discord
from asgiref.sync import sync_to_async
from django.db.models import Count, Max
from commands.interractions.resultmessageshower import ResultmessageShower
from commands.sendable import Sendable
from commands.utils.utils import getworldbosstime
from api.highscores.models import Highscore
from api.ingame_data.models import Encounter, Chest, Roll, Activity
from utils.tablify_dict import tablify_dict


async def lastonline(sendable: Sendable, playername: str=None):
    if playername is not None:
        func = sync_to_async(Activity.objects.get)
        try:
            activity_obj: Activity = await func(player__iexact=playername)
            await sendable.send(f"{activity_obj.player} was last online at {activity_obj.get_lastonline()}")
        except Activity.DoesNotExist:
            await sendable.send(f"I have no information on when {playername} was last online.")
            return
    else:
        func = sync_to_async(Activity.objects.aggregate)
        highest_lastonline = await func(Max('lastonline'))
        highest_lastonline = highest_lastonline["lastonline__max"]
        await sendable.send(f"last online check was at <t:{int(highest_lastonline.timestamp())}>")


async def getencounters(sendable: Sendable, searchtype: str, name: str=None):
    """
    gets the encounters
    :param ctx: message context
    :param name: either playername, pokemonname or a date
    """
    if searchtype == "topdates":
        qs = Encounter.objects.values('date').annotate(count=Count('date')).order_by('-count')
    elif searchtype == "topplayers":
        qs = Encounter.objects.values('player').annotate(count=Count('player')).order_by('-count')
    elif searchtype == "toppokemon":
        qs = Encounter.objects.values('pokemon').annotate(count=Count('pokemon')).order_by('-count')
    elif name is None:
        await sendable.send("Please provide an argument or pick another searchtype!")
        return
    elif searchtype == "pokemon":
        qs = Encounter.objects.filter(pokemon__iexact=name).order_by("date")
    elif searchtype == "date":
        qs = Encounter.objects.filter(date=name)
    elif searchtype == "player":
        qs = Encounter.objects.filter(player__iexact=name).order_by("date")
    else:
        raise ValueError(f"invalid searchtype: {searchtype}")
    values = [value async for value in qs]
    if values and hasattr(values[0], "to_json"):
        values = [value.to_json() for value in values]
    messages = tablify_dict(values)
    await sendable.send(content=messages[0],
                         view=ResultmessageShower(messages, sendable))


async def getchests(sendable: Sendable, searchtype, argument: str=None):
    if searchtype == "topdates":
        qs = Chest.objects.values('date').annotate(count=Count('date')).order_by('-count')
    elif searchtype == "topplayers":
        qs = Chest.objects.values('player').annotate(count=Count('player')).order_by('-count')
    elif searchtype == "toplocations":
        qs = Chest.objects.values('location').annotate(count=Count('location')).order_by('-count')
    elif argument is None:
        await sendable.send("Please provide an argument or pick another searchtype!")
        return
    elif searchtype == "location":
        qs = Chest.objects.filter(location__iexact=argument).order_by("date")
    elif searchtype == "date":
        qs = Chest.objects.filter(date=argument)
    elif searchtype == "player":
        qs = Chest.objects.filter(player__iexact=argument).order_by("date")
    else:
        raise ValueError(f"invalid searchtype: {searchtype}")

    values = [value async for value in qs]

    if values and hasattr(values[0], "to_json"):
        values = [value.to_json() for value in values]
    messages = tablify_dict(values)
    await sendable.send(content=messages[0],
                        view=ResultmessageShower(messages, sendable))


async def getrolls(sendable: Sendable, searchtype, parameter: str=None):
    """
    Gets the rolls of a player, the rolls of a pokemon, or the rolls on a specific date.
    Timeout is 10 minutes, then the message gets deleted.
    :param ctx: discord context
    :param parameter: The pokemon, date or player
    """
    if searchtype == "topdates":
        qs = Roll.objects.values('date').annotate(count=Count('date')).order_by('-count')
    elif searchtype == "topplayers":
        qs = Roll.objects.values('player').annotate(count=Count('player')).order_by('-count')
    elif searchtype == "toppokemon":
        qs = Roll.objects.values('pokemon').annotate(count=Count('pokemon')).order_by('-count')
    elif parameter is None:
        await sendable.send("Please provide an argument or pick another searchtype!")
        return
    elif searchtype == "pokemon":
        qs = Roll.objects.filter(pokemon__iexact=parameter).order_by("date")
    elif searchtype == "date":
        qs = Roll.objects.filter(date=parameter)
    elif searchtype == "player":
        qs = Roll.objects.filter(player__iexact=parameter).order_by("date")
    else:
        raise ValueError(f"invalid searchtype: {searchtype}")
    values = [value async for value in qs]
    if values and hasattr(values[0], "to_json"):
        values = [value.to_json() for value in values]
    messages = tablify_dict(values)
    await sendable.send(content=messages[0],
                        view=ResultmessageShower(messages, sendable))


async def getclanencounters(sendable: Sendable, clanname: str):
    usernames = set([value.data["username"] async for value in
                 Highscore.objects.filter(data__clan__iexact=clanname, data__has_key="username")])
    values = [value.to_json() async for value in Encounter.objects.filter(player__in=usernames).order_by("-date")]
    messages = tablify_dict(values, order=["date", "player", "pokemon"], max_length=1800)
    resultmessageshower = ResultmessageShower(messages, sendable)
    await sendable.send(
        content=f"page {resultmessageshower.currentpage} of {resultmessageshower.maxpage}\n" + messages[0],
        view=resultmessageshower)


async def worldbosstime(sendable: Sendable):
    """
    @todo unity will impact this.
    gives the time untill the start of the worldboss.
    :param ctx: discord context
    """
    try:
        worldboss_datetime = getworldbosstime()
        timedifference = worldboss_datetime - datetime.datetime.now()
        embed = discord.Embed(title="worldboss",
                              description=f"The worldboss will start at <t:{str(int(worldboss_datetime.timestamp()))}>")
        embed.add_field(name="relative",
                        value=f"that is in {(timedifference.days * 86400 + timedifference.seconds) // 3600} hours "
                              f"and {(timedifference.seconds // 60) % 60} minutes\n")
        await sendable.send(embed=embed)
    except IndexError:
        await sendable.send("something went wrong!")
    except Exception as e:
        await sendable.send("uncaught exception.")
        raise e
