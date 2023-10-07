import asyncio
import datetime
import json
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import discord
from asgiref.sync import sync_to_async

from commands.interractions.miscellaneous.help_cmd import HelpCmd
from commands.interractions.resultmessageshower import ResultmessageShower
from commands.interractions.selectsview import SelectsView
from commands.sendable import Sendable
from api.highscores.models import Highscore, WorldbossHighscore, DefaultClanname

from ppobyter.marketplace.item import Item
from ppobyter.marketplace.pokemon import Pokemon
from utils.tablify_dict import tablify_dict


# def __generate_img(pokemon: Pokemon):
#     # all sprites come from https://github.com/PokeAPI/sprites
#     if pokemon is None:
#         print("warning: None")
#         return
#     img = Image.open(r"base_pokemon.png")
#     draw = ImageDraw.Draw(img)
#     font = ImageFont.truetype(r"memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS-muw.ttf",
#                               15)
#     # font = ImageFont.load_default()
#     draw.text((79, 478), pokemon.helditem, (255, 255, 255), font=font)  # held item
#     draw.text((363, 95), f"{pokemon.pokemonnumber}", (255, 255, 255), font=font)  # pokemon number
#     draw.text((83, 375), f"Lv {pokemon.level} {pokemon.pokemonname}", font=font)
#     draw.text((363, 172), pokemon.nature, (255, 255, 255), font=font)  # nature
#     draw.text((363, 210), f"{pokemon.happiness}", (255, 255, 255), font=font)  # happiness
#     draw.text((363, 247), f"{pokemon.ability}", (255, 255, 255), font=font)  # ability
#     draw.text((363, 285), pokemon.catcher, (255, 255, 255), font=font)  # catcher
#     draw.text((363, 331), f"{pokemon.hp}", (255, 255, 255), font=font)  # calculated hp
#     draw.text((363, 408), f"{pokemon.atk}", (255, 255, 255), font=font)  # calculated atk
#     draw.text((363, 445), f"{pokemon.defense}", (255, 255, 255), font=font)  # calculated def
#     draw.text((363, 484), f"{pokemon.spatk}", (255, 255, 255), font=font)  # calculated spatk
#     draw.text((363, 520), f"{pokemon.spdef}", (255, 255, 255), font=font)  # calculated spdef
#     draw.text((363, 557), f"{pokemon.speed}", (255, 255, 255), font=font)  # calculated speed
#
#     draw.text((400, 331), f"({pokemon.hpiv})", (219, 225, 165), font=font)  # hp iv
#     draw.text((400, 408), f"({pokemon.atkiv})", (219, 225, 165), font=font)  # atk iv
#     draw.text((400, 445), f"({pokemon.defiv})", (219, 225, 165), font=font)  # def iv
#     draw.text((400, 484), f"({pokemon.spatkiv})", (219, 225, 165), font=font)  # spatk iv
#     draw.text((400, 520), f"({pokemon.spdefiv})", (219, 225, 165), font=font)  # spdef iv
#     draw.text((400, 557), f"({pokemon.speediv})", (219, 225, 165), font=font)  # speed iv
#
#     draw.text((435, 331), f"({pokemon.hpev})", (182, 219, 180), font=font)  # hp ev
#     draw.text((435, 408), f"({pokemon.atkev})", (182, 219, 180), font=font)  # atk ev
#     draw.text((435, 445), f"({pokemon.defev})", (182, 219, 180), font=font)  # def ev
#     draw.text((435, 484), f"({pokemon.spatkev})", (182, 219, 180), font=font)  # spatk ev
#     draw.text((435, 520), f"({pokemon.spdefev})", (182, 219, 180), font=font)  # spdef ev
#     draw.text((435, 557), f"({pokemon.speedev})", (182, 219, 180), font=font)  # speed ev
#     try:  # adding sprite of the pokemon.
#         sprite = Image.open(r"sprites/pokemon/" + str(pokemon.pokemonnumber) + ".png")
#         sprite = sprite.resize((200, 200))
#         for y in range(sprite.height):
#             for x in range(sprite.width):
#                 pixel = sprite.getpixel((x, y))
#                 if pixel == 0 or pixel == 9:
#                     sprite.putpixel((x, y), (233, 235, 233))
#         img.paste(sprite, (48, 128))
#     except Exception as e:
#         print(f"exception with {pokemon.pokemonname} when adding sprite for pokemon", e)
#     if pokemon.helditem != "none":
#         try:
#             helditem = Image.open(r"sprites/items/" + str(pokemon.helditem.lower()).replace(" ", "-") + ".png")
#             helditem = helditem.resize((46, 44))
#             img.paste(helditem, (22, 470))
#         except Exception as e:
#             print(f"exception when adding held item. Held item: {pokemon.helditem}", e)
#     return img


async def clanlist(sendable: Sendable, clanname: str):
    """
    gives a list of players that are in the provided clan. @todo test this with filled highscores database
    :param ctx: discord context
    :param clanname: the name of the clan you want the clanlist from.
    """
    players = list(set([highscore.data["username"] async for highscore in Highscore.objects.filter(data__clan__iexact=clanname, data__has_key="username")]))
    if players:
        await sendable.send(f"clanlist of {clanname}: \n" + ", ".join(players))
    else:
        await sendable.send("no results found for that clanname.")


async def invite(sendable: Sendable):
    invitelink = "https://discord.com/login?redirect_to=" \
            "%2Foauth2%2Fauthorize%3Fclient_id%3D733434249771745401%26permissions%3D2048%26redirect_uri" \
            "%3Dhttps%253A%252F%252Fdiscordapp.com%252Foauth2%252Fauthorize%253F%2526" \
            "permissions%253D141312%2526client_id%253D733434249771745401%2526scope%253Dbot%26scope%3Dbot"
    embed = discord.Embed()
    embed.description = "this is the [invite link]" \
                        "({})" \
                        "\n also join the [support server](https://discord.gg/PmXY35aqgH)".format(invitelink)

    await sendable.send(embed=embed)


async def setdefault(sendable: Sendable, clanname: str = None):
    """
    sets a default for the highscores commands. If the clanname is not provided the default will be removed.
    :param sendable: sendable
    :param clanname: the clan you want to set as default for the highscores commands.
    """
    if sendable.guild is None:
        await sendable.send("this command can't be used in pm.")
        return
    elif not sendable.user.guild_permissions.administrator:
        await sendable.send(
            "insufficient permissions to use this command. Ask a server administrator!")
        return
    try:
        defaultclannameobj: DefaultClanname = await DefaultClanname.objects.aget(guild=sendable.guild.id)
    except DefaultClanname.DoesNotExist:
        defaultclannameobj = DefaultClanname(guild=sendable.guild.id, clan=clanname)

    if clanname is None:
        await (sync_to_async(defaultclannameobj.delete))()
        await sendable.send("Default clanname for highscores commands removed!")
    else:  # clanname provided.
        await (sync_to_async(defaultclannameobj.save))()
        await sendable.send(f"default clanname for highscores set to `{clanname}`!")


# async def worldboss(sendable: Sendable, playername: str):
#     """
#     shows a list of worldbosses a player participated in.
#     :param ctx: discord context
#     :param playername: the player of who you want to see the worldbosses he/she participated in.
#     """
#     values = []
#     async for i in WorldbossHighscore.objects.filter(player=playername).order_by("worldboss__date"):
#         wbhighscore = i.to_json()
#         wb = await (sync_to_async(i.get_worldboss))()
#         wbhighscore.update(wb.to_json())
#         values.append(wbhighscore)
#
#     messages = tablify_dict(values, order=["player", "pokemon", "damage", "rank", "participants", "date"],
#                             verbose_names={"pokemon": "worldboss"}, max_length=1900)
#     messageshower = ResultmessageShower(messages, sendable)
#     await sendable.send(f"page {messageshower.currentpage} of {messageshower.maxpage}\n" +
#                         messages[messageshower.currentpage-1], view=messageshower)
