from typing import List

from discord import Interaction
import discord

from commands.interractions.resultmessageshower import ResultmessageShower
from commands.interractions.selectsutility import SelectsUtility
from commands.utils.utils import tablify
from highscores import Btwinstreak, Btwins, getClanList, allhighscores


class TopCommand(SelectsUtility):
    def __init__(self, interaction: Interaction, highscores: List[str], clanname: str):
        super().__init__(interaction=interaction, options=highscores, max_selectable=1, min_selectable=1,
                         placeholder="select the highscore you want to see")
        self.clanname = clanname
        self.highscores = highscores

    async def callback(self, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        highscorename = self.values[0]
        for highscore in allhighscores:
            highscore = highscore()
            if highscore.NAME == highscorename:
                break
        else:
            raise ValueError(f"Highscore {highscorename} does not exist!!")
        if highscorename == "btwins" or highscorename == "btwinstreak":
            values = []
            clanlist = getClanList(self.clanname.lower()) if self.clanname is not None else []
            highscore = Btwinstreak() if highscorename == "btwinstreak" else Btwins()
            for row in highscore.getDbValues():
                if row[1] in clanlist or row[0] < 10:
                    values.append(row)
        else:
            try:
                values = highscore.getDbValues(query="SELECT * FROM {0} WHERE clan=? OR rank<10".format(highscore.NAME),
                                               params=[(self.clanname.lower() if self.clanname is not None else None)])
            except Exception as e:
                print(e)
                values = highscore.getDbValues(query="SELECT * FROM {0} WHERE rank<10".format(highscore.NAME))
        messages = tablify(highscore.LAYOUT, values, maxlength=1930)
        await interaction.response.send_message(content=messages[0],
                                                     view=ResultmessageShower(messages, interaction=interaction))

