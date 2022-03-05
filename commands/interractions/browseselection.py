import discord
from discord.ext.commands import Context


class BrowseSelection(discord.ui.View):
    """
    handles the buttons to browse through something.
    """
    def __init__(self, ctx: Context, pagesamount: int, ownerOnly=True):
        """
        constructor
        :param ctx: discord context.
        :param pagesamount: amount of pages.
        :param ownerOnly: if only the owner/initiator may press the buttons.
        """
        super().__init__()
        self.ownerOnly = ownerOnly
        self.ctx = ctx
        self.currentpage = 1
        self.maxpage = pagesamount

    @discord.ui.button(label='<<', style=discord.ButtonStyle.green)
    async def minpage(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        set current page to 1.
        :param button:
        :param interaction:
        :return:
        """
        if not await self.isOwner(interaction): return
        self.currentpage = 1
        await self._sendPage(interaction)

    @discord.ui.button(label='<', style=discord.ButtonStyle.green)
    async def previouspage(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        go 1 page back (if possible)
        :param button:
        :param interaction:
        :return:
        """
        if not await self.isOwner(interaction): return
        if self.currentpage - 1 >= 1:
            self.currentpage -= 1
        await self._sendPage(interaction)

    @discord.ui.button(label='>', style=discord.ButtonStyle.danger)
    async def nextpage(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        go to the next page (if possible)
        :param button:
        :param interaction:
        :return:
        """
        if not await self.isOwner(interaction): return
        if self.currentpage + 1 <= self.maxpage:
            self.currentpage += 1
        await self._sendPage(interaction)

    @discord.ui.button(label='>>', style=discord.ButtonStyle.danger)
    async def maxpage(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        go to the max page.
        :param button:
        :param interaction:
        :return:
        """
        if not await self.isOwner(interaction): return
        self.currentpage = self.maxpage
        await self._sendPage(interaction)

    async def _sendPage(self, interaction: discord.Interaction):
        """
        to be implemented by subclasses.
        What gets sent on any button press.
        :param interaction:
        :return:
        """
        raise NotImplementedError

    async def isOwner(self, interaction: discord.Interaction) -> bool:
        """
        :param interaction:
        :return: if the interaction is made by the owner.
        """
        if not self.ownerOnly:
            return True
        if interaction.guild != self.ctx.guild or interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("only the user who used the command can use these buttons!")
            return False
        return True
