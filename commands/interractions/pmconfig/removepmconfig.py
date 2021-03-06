import sqlite3

import discord
from discord import Interaction
from discord.ext.commands import Context

from commands.interractions.selectsutility import SelectsUtility
from commands.interractions.selectsview import SelectsView


class EventSelection(SelectsUtility):
    def __init__(self, interaction: Interaction, onSelection):
        super().__init__(interaction, ["goldrush", "swarm", "worldboss", "honey", "tournament"], max_selectable=1,
                         min_selectable=1, placeholder="select the event to unregister for:")
        self.onSelection = onSelection

    async def callback(self, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        await self.onSelection(self.values[0], interaction)


class EventRemoval(SelectsUtility):
    def __init__(self, interaction, options, alloptions, eventname, indexes, databasepath):
        super(EventRemoval, self).__init__(interaction, options, max_selectable=1)
        self.alloptions = alloptions
        self.indexes = indexes
        self.eventname = eventname
        self.databasepath = databasepath

    async def callback(self, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        index = self.alloptions.index(self.values[0])
        if self.eventname == "swarm":
            query = "DELETE FROM pmswarm WHERE playerid=? AND pokemon IS ? AND location IS ? AND comparator=?"
        elif self.eventname == "goldrush":
            query = "DELETE FROM pmgoldrush WHERE playerid=? AND location=?"
        elif self.eventname == "worldboss":
            query = "DELETE FROM pmworldboss WHERE playerid = ? AND boss IS ? AND location IS ? AND comparator=?"
        elif self.eventname == "tournament":
            query = "DELETE FROM pmtournament WHERE playerid=? AND tournament IS ? AND prize IS ? AND comparator=?"
        elif self.eventname == "honey":
            query = "DELETE FROM pmhoney WHERE playerid=? AND location=?"
        else:
            raise ValueError(f"{self.values[0]} is an invalid value!!")
        conn = sqlite3.connect(self.databasepath)
        cur = conn.cursor()
        result = cur.execute(query, [self.interaction.user.id] + list(self.indexes[index]))
        conn.commit()
        conn.close()
        if result.rowcount:
            await interaction.response.send_message(content="configuration removed!")
        else:
            await interaction.response.send_message(content="something went wrong. Sending debug info...")
            raise ValueError(f"failed to remove config {str(self.indexes[index])} userid: {self.interaction.user.id}"
                             f" event: {self.eventname}")

class RemovePmConfig(discord.ui.View):
    def __init__(self, interaction, databasepath):
        super().__init__()
        self.databasepath = databasepath
        self.add_item(EventSelection(interaction, self.onSelection))
        self.interaction = interaction

    async def startremoval(self):
        await self.interaction.response.send_message("select the event to unregister for:", view=self)
    
    async def onSelection(self, event, interaction):
        conn = sqlite3.connect(self.databasepath)
        cur = conn.cursor()
        if event == "swarm":
            cur.execute("SELECT pokemon, location, comparator FROM pmswarm WHERE playerid = ?", (self.interaction.user.id,))
            layout = ["pokemon", "location", "comparator"]
        elif event == "goldrush":
            cur.execute("SELECT location FROM pmgoldrush WHERE playerid = ?", (self.interaction.user.id,))
            layout = ["location"]
        elif event == "honey":
            cur.execute("SELECT location FROM pmhoney WHERE playerid = ?", (self.interaction.user.id,))
            layout = ["location"]
        elif event == "tournament":
            cur.execute("SELECT tournament, prize, comparator FROM pmtournament WHERE playerid=?", (self.interaction.user.id,))
            layout = ["tournament", "prize", "comparator"]
        elif event == "worldboss":
            cur.execute("SELECT boss, location, comparator FROM pmworldboss WHERE playerid=?", (self.interaction.user.id,))
            layout = ["worldboss", "location", "comparator"]
        else:
            raise ValueError(f"invalid event {event}!")
        messages = []
        indexes = []
        result = cur.fetchall()
        conn.close()
        for row in result:
            message = ""
            for index, val in enumerate(layout):
                message += f"{val}: {row[index]}, "
            if message not in messages:
                messages.append(message)
                indexes.append(row)
        await interaction.response.send_message("what event do you want to remove?",
                            view=SelectsView(self.interaction, messages,
                                             lambda options: self.selectoptionsbuilder(options, messages, event, indexes)))

    def selectoptionsbuilder(self, options, messages, eventname, indexes):
        return EventRemoval(self.interaction, options, messages, eventname, indexes, self.databasepath)
