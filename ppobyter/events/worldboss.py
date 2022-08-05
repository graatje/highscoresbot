import sqlite3
import time
import datetime

import pyautogui
from .event import Event


class Worldboss(Event):
    """
    This event gets triggered when a worldboss shows up.
    """
    def __init__(self, location: str, pokemon: str):
        """
        Calls superclass init, presses powerticket, inserts worldboss.
        :param location: the location where the worldboss showed up.
        :param pokemon: The worldboss that showed up.
        """
        self.location = location.lower()
        self.pokemon = pokemon.lower()
        self.EVENTNAME = "worldboss"
        super(Worldboss, self).__init__()
        self.presspowerticket()

    def makeMessage(self) -> str:
        """
        Makes the message that gets sent to the recipients.
        :return: the message
        """
        return f"A {self.pokemon} World Boss has been spotted at {self.location}!"

    def determineRecipients(self, **kwargs):
        """
        Determines pmrecipients and channelrecipients.
        """
        self._determinechannelrecipients()
        self.__determinepmrecipients()

    def presspowerticket(self):
        """
        presses the powerticket.
        """
        for i in range(2):
            try:
                pyautogui.click(300, 420, clicks=2)
                time.sleep(0.2)
            except Exception as e:
                print(e)
                print("failed to press ticket.")

    def __determinepmrecipients(self):
        """
        Determines the pmrecipients based on worldboss pokemon, location or a combination of both.
        """
        conn = sqlite3.connect(self.pathManager.getpath("eventconfigurations.db"))
        cur = conn.cursor()
        cur.execute("SELECT playerid FROM pmworldboss WHERE location=? AND boss=? AND comparator='&'",
                    (self.location, self.pokemon))
        playerids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT playerid FROM pmworldboss WHERE (location=? OR boss=?) AND comparator='|'",
                    (self.location, self.pokemon))
        playerids += [row[0] for row in cur.fetchall()]
        conn.close()
        self._pmrecipients = list(set(playerids))
