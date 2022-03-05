from typing import Callable, Coroutine, Awaitable

import discord
from discord.ext.commands import Context


class PlayerConfig(discord.ui.View):
    """
    view for the playerconfig command.
    """
    def __init__(self, add: Callable[[Context], Awaitable[None]], remove: Callable[[Context], Awaitable[None]],
                 show: Callable[[Context], Awaitable[None]], ctx: Context):
        """

        :param add: callable for adding a player to playerconfig
        :param remove: callable for removing a player from playerconfig
        :param show: callable for showing playerconfig
        :param ctx:
        """
        super().__init__()
        self.add = add
        self.remove = remove
        self.show = show
        self.ctx = ctx

    @discord.ui.button(label='add player', style=discord.ButtonStyle.green)
    async def addplayer(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.isOwner(interaction):return
        await interaction.response.edit_message(content="interaction starting.", view=None)
        await interaction.delete_original_message()
        await self.add(self.ctx)
        self.stop()

    @discord.ui.button(label='remove player', style=discord.ButtonStyle.danger)
    async def removeplayer(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        await interaction.response.edit_message(content="interaction starting.", view=None)
        await interaction.delete_original_message()
        await self.remove(self.ctx)
        self.stop()

    @discord.ui.button(label='show playerconfigurations', style=discord.ButtonStyle.blurple)
    async def showplayers(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not await self.isOwner(interaction): return
        await interaction.response.edit_message(content="interaction starting.", view=None)
        await interaction.delete_original_message()
        await self.show(self.ctx)
        self.stop()

    async def isOwner(self, interaction: discord.Interaction) -> bool:
        if interaction.guild.id != self.ctx.guild.id or interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("only the user who used the command can use these buttons!")
            return False
        return True
