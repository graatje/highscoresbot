import sqlite3
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
