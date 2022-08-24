from typing import Union
from asgiref.sync import sync_to_async
from db.highscores.models import Highscore, HighscoreConfig, DefaultClanname
from commands.interractions.highscore_command import HighscoreCommand
from commands.interractions.resultmessageshower import ResultmessageShower
from commands.sendable import Sendable
from commands.utils.utils import joinmessages
from utils.tablify_dict import tablify_dict


async def get_highscore_config(highscorename):
    func = sync_to_async(HighscoreConfig.objects.get)
    return await func(highscorename=highscorename)


async def getdefaultclanname(interaction) -> Union[str, None]:
    if interaction.guild is None:
        return None
    try:
        return (await DefaultClanname.objects.aget(guild=interaction.guild.id)).clan
    except DefaultClanname.DoesNotExist:
        return None


async def getplayer(sendable: Sendable, username: str):
    """
    gets a collection of highscores a player is in.
    :param sendable: the Sendable object.
    :param username: the name of the player you want info from.
    """
    messages = []
    async for highscoredata in Highscore.objects.filter(data__username__iexact=username):
        func = sync_to_async(highscoredata.get_highscore_config)
        highscoreconfig = await func()
        messages.append(highscoreconfig.verbose_name)
        messages += tablify_dict([highscoredata.to_json()], order=["rank", "username", "clan"])
    messages = joinmessages(messages)

    if len(messages) == 0:
        await sendable.send("or {0} is not in any highscore or he does not exist.".format(username))
    else:
        view = ResultmessageShower(messages, sendable)
        await sendable.send(messages[0], view=view)


async def getclan(sendable: Sendable, clanname: str = None):
    # if the clanname is None and the default is also not present we set the clanname to an empty string.
    # if it is present tho the clanname gets set to the default.
    if clanname is None and (clanname := await getdefaultclanname(interaction=sendable)) is None:
        clanname = ""
    highscores = ["ancientcavemapcontrol", "battlezonemapcontrol", "safarizonemapcontrol", "toprichestclans",
                  "clanwarwins", "topstrongestclans"]
    messages = []
    for highscorename in highscores:
        highscoreconfig = await get_highscore_config(highscorename)

        qs = Highscore.objects.filter(highscore=highscoreconfig, data__clan__iexact=clanname).order_by('rank')
        values = [value.to_json() async for value in qs]
        if not values:
            continue
        messages.append(highscoreconfig.verbose_name)
        messages += tablify_dict(values,
                                 verbose_names=dict(highscoreconfig.fieldmapping), order=["rank", "clan"])
    messages = joinmessages(messages)
    if not messages:
        await sendable.send(f"The clan {clanname} is not in the highscores or does not exist.")
        return

    view = ResultmessageShower(messages, sendable)
    await sendable.send(messages[0], view=view)


async def top(sendable: Sendable, highscorename, clanname: str=None):
    """
    shows top 9 + the provided clan if available.
    :param ctx: discord context
    :param clanname: the clanname, default none, clannamehandler gets clan from db if none.
    """
    # if the clanname is None and the default is also not present we set the clanname to an empty string.
    # if it is present tho the clanname gets set to the default.
    if clanname is None and (clanname := await getdefaultclanname(interaction=sendable)) is None:
        clanname = ""
    highscoreconfig = await get_highscore_config(highscorename)
    qs = Highscore.objects.filter(highscore=highscoreconfig, rank__lt=10).order_by('rank') | \
         Highscore.objects.filter(highscore=highscoreconfig, data__clan__iexact=clanname).order_by('rank')
    messages = tablify_dict([value.to_json() async for value in qs],
                            order=["rank", "username", "clan"],
                            verbose_names=dict(highscoreconfig.fieldmapping))
    view = ResultmessageShower(messages, sendable)
    await sendable.send(messages[0], view=view)


async def highscore(sendable: Sendable, highscorename: str, clanname: str = None):
    # if the clanname is None and the default is also not present we set the clanname to an empty string.
    # if it is present tho the clanname gets set to the default.
    if clanname is None:
        clanname = await getdefaultclanname(interaction=sendable)
    view = HighscoreCommand(sendable, highscorename, clanname)
    await view.init()
    await sendable.send(await view.getPage(), view=view)


async def mapcontrol(sendable: Sendable, clanname: str = None):
    """
    shows the standings of all mapcontrol areas.
    :param ctx: discord context
    :param clanname: the name of the clan, optional.
    """
    # if the clanname is None and the default is also not present we set the clanname to an empty string.
    # if it is present tho the clanname gets set to the default.
    if clanname is None and (clanname := await getdefaultclanname(interaction=sendable)) is None:
        clanname = ""
    mapcontrolhighscores = ["ancientcavemapcontrol", "battlezonemapcontrol", "safarizonemapcontrol"]
    messages = []
    for highscorename in mapcontrolhighscores:
        highscoreconfig = await get_highscore_config(highscorename)
        qs = Highscore.objects.filter(highscore=highscoreconfig, rank__lt=10).order_by('rank') | \
             Highscore.objects.filter(highscore=highscoreconfig, data__clan__iexact=clanname).order_by('rank')

        messages += tablify_dict([value.to_json() async for value in qs],
                                 verbose_names=dict(highscoreconfig.fieldmapping))
    messages = joinmessages(messages)
    view = ResultmessageShower(messages, sendable)
    await sendable.send(messages[0], view=view)
