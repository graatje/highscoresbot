import sqlite3
from sqlite3 import Cursor
from typing import List, Union

import discord

from ppobyter.events.event import Event
from ppobyter.marketplace.item import Item


# @todo this needs a complete rewrite
class GMSearch(Event):
    def __init__(self, searcheditems: List[Item]):
        pass
