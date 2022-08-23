from typing import List

import discord
from discord.ui import TextInput

from db.config.models import Eventname
from db.eventconfigurations.models import PmConfig

class PmConfigModel(discord.ui.Modal, title="MINE"):
    def __init__(self, textinputs: List[TextInput], event: Eventname):
        super().__init__()
        self.event = event
        self.textinputs: List[TextInput] = textinputs
        for textinput in self.textinputs:
            self.add_item(textinput)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        #@todo input validation.
        data = {}
        for i in self.textinputs:
            if i.value == "":
                continue
            data[i.custom_id] = i.value
        await PmConfig.objects.acreate(event=self.event, user=interaction.user.id,
                                data=data)
        await interaction.response.send_message(f"condition for {self.event.name} showing up added!")
