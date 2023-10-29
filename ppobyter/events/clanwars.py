import datetime
from typing import Union

import discord

from ppobyter.events.event import Event


class Clanwars(Event):
    """
    Clan Wars is an event held two times every Saturday and Sunday. Clan Wars start at 7:00PM and 7:50PM UTC
    (Tier 1 and Tier 2 respectively).
    """
    def __init__(self, tier: int, minstillstart: int):
        self.EVENTNAME = "clanwars"
        self.currenttier = 1
        super().__init__()
        self.tier = tier
        self.minstillstart = minstillstart

    def makeMessage(self) -> str:
        return f"tier {self.tier} of clan wars is starting in {self.minstillstart} minutes."

    def determineRecipients(self, **kwargs):
        """
        determines the recipients for the event.
        :param kwargs: none required
        """
        self._determinechannelrecipients()
