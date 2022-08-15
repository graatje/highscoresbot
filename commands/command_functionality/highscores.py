import sqlite3
from typing import Union, List, Dict
from asgiref.sync import sync_to_async
from db.highscores.models import Highscore, HighscoreConfig
from commands.interractions.highscore_command import HighscoreCommand
from commands.interractions.resultmessageshower import ResultmessageShower
from commands.interractions.selectsview import SelectsView
from commands.interractions.top_command import TopCommand
from commands.sendable import Sendable
from commands.utils.utils import joinmessages, tablify
from config import Config
from utils.tablify_dict import tablify_dict


async def get_highscore_config(highscorename):
    func = sync_to_async(HighscoreConfig.objects.get)
    return await func(highscorename=highscorename)


async def getdefaultclanname(interaction, comment=True) -> Union[str, None]:
    if interaction.guild is None:
        return
    conn = sqlite3.connect("highscores.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM clannames WHERE id=?", (interaction.guild.id,))
    try:
        clanname = cur.fetchall()[0][0]
    except IndexError:
        clanname = None
    if clanname is None and comment:
        await interaction.response.send_message("Please register a default clanname or provide a clan in the command.")
    elif clanname is not None:
        clanname = clanname.lower()
    return clanname


async def getplayer(sendable: Sendable, username: str):
    """
    gets a collection of highscores a player is in.
    :param ctx: discord context
    :param username: the name of the player you want info from.
    """
    \
    allmessages = []
    for playerhighscore in playerresp.json():
        fieldmapping = highscoresrespjson[playerhighscore["highscore"]]
        layout = ["Rank"]
        values = [str(playerhighscore["rank"])]
        for key, value in fieldmapping.items():
            layout.append(str(value))
            values.append(str(playerhighscore[key]))
        allmessages.append(tablify(layout, [values])[0])
    allmessages = joinmessages(allmessages)

    if len(allmessages) == 0:
        await sendable.send("or {0} is not in any highscore or he does not exist.".format(username))
    else:
        view = ResultmessageShower(allmessages, sendable)
        await sendable.send(allmessages[0], view=view)


async def getclan(sendable: Sendable, clanname: str):
    clanname = clanname.lower()
    getclanhighscores = [(SafariMapcontrol, "Safari zone mapcontrol"),
                         (AncMapcontrol, "Ancient cave mapcontrol"),
                         (BzMapcontrol, "Battle zone mapcontrol"),
                         (BestClans, "Top clan experience"),
                         (RichestClans, "Top richest clans")]
    allmessages = []
    for highscore, name in getclanhighscores:
        highscore = highscore()
        values = highscore.getDbValues(f"SELECT * FROM {highscore.NAME}")
        for i in values:
            if i[1] == clanname:
                allmessages.append(name)
                allmessages += tablify(highscore.LAYOUT, [i])
                break
    allmessages = joinmessages(allmessages)
    if not allmessages:
        await sendable.send(f"The clan {clanname} is not in the highscores or does not exist.")
        return

    view = ResultmessageShower(allmessages, sendable)
    await sendable.send(allmessages[0], view=view)


async def top(sendable: Sendable, clanname: str=None):
    """
    shows top 9 + the provided clan if available.
    :param ctx: discord context
    :param clanname: the clanname, default none, clannamehandler gets clan from db if none.
    """
    highscoresdict = {}
    for highscore in allhighscores:
        highscore = highscore()
        highscoresdict[highscore.NAME] = highscore

    def highscoreselectionmaker(highscores):
        return TopCommand(sendable, highscores, clanname)

    view = SelectsView(sendable, highscoresdict, highscoreselectionmaker)
    await sendable.send(content=f"page {view.currentpage} of {view.maxpage}", view=view)


async def highscore(sendable: Sendable, clanname: str=None):
    initializedhighscores = {}
    for highscore in allhighscores:
        highscore = highscore()
        initializedhighscores[highscore.NAME] = highscore

    def highscoreselectionmaker(highscores):
        return HighscoreCommand(sendable, highscores, clanname=clanname)

    view = SelectsView(sendable, initializedhighscores.keys(), highscoreselectionmaker)
    await sendable.send(content=f"page {view.currentpage} of {view.maxpage}", view=view)


async def mapcontrol(sendable: Sendable, clanname: str=None):
    """
    shows the standings of all mapcontrol areas.
    :param ctx: discord context
    :param clanname: the name of the clan, optional.
    """

    if clanname is None:
        clanname = ""
    mapcontrolhighscores = ["ancientcavemapcontrol", "battlezonemapcontrol", "safarizonemapcontrol"]
    messages = []
    for highscorename in mapcontrolhighscores:
        highscoreconfig = await get_highscore_config(highscorename)
        qs = Highscore.objects.filter(highscore=highscoreconfig, rank__lt=10).order_by('rank') | \
             Highscore.objects.filter(highscore=highscoreconfig, data__clan=clanname).order_by('rank')

        messages += tablify_dict([value.to_json() async for value in qs],
                                 verbose_names=dict(highscoreconfig.fieldmapping))
    messages = joinmessages(messages)
    view = ResultmessageShower(messages, sendable)
    await sendable.send(messages[0], view=view)
