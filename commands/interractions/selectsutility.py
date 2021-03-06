from typing import List

import discord
from discord import Interaction


class SelectsUtility(discord.ui.Select):
    def __init__(self, interaction: Interaction, options: List[str], max_selectable: int, min_selectable=1, placeholder="select below:",
                 ownerOnly=True):
        self.ownerOnly = ownerOnly
        self.interaction = interaction
        if len(options) > 25:
            raise ValueError("A select can't contain more than 25 items!")
        selectoptions = [discord.SelectOption(label=option) for option in options]
        super().__init__(placeholder=placeholder, min_values=min_selectable,
                         max_values=max_selectable,
                         options=selectoptions)

    async def callback(self, interaction: discord.Interaction):
        raise NotImplementedError

    async def isOwner(self, interaction: discord.Interaction) -> bool:
        if not self.ownerOnly:
            return True
        if interaction.guild != self.interaction.guild or interaction.user.id != self.interaction.user.id:
            await interaction.response.send_message("only the user who used the command can use these buttons!")
            return False
        return True
