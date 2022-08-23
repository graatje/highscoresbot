from typing import List

import discord
from discord import TextInput


class PmConfigModel(discord.ui.Modal, title="MINE"):
    def __init__(self, textinputs: List[TextInput]):
        super().__init__()
        self.textinputs: List[TextInput] = textinputs
        for textinput in self.textinputs:
            self.add_item(textinput)


    async def on_submit(self, interaction: discord.Interaction) -> None:
        for i in self.textinputs:
            print(i.value)
        print("hello")
        # Now we can access similar to a classvar
    #    print(self.my_item.value)
