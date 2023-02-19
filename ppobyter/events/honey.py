from api.eventconfigurations.models import PmConfig
from .event import Event


class Honey(Event):
    """
    This is an event that happens when a player spreads honey at a location.
    """
    def __init__(self, location: str, player: str):
        """
        Here the init of the superclass is called, the location is inserted, the player and location properties get set.
        :param location: the location honey is spread at.
        :param player: The player who spread the honey.
        """
        self.location = location.lower()
        self.player = player
        self.EVENTNAME = "honey"
        super(Honey, self).__init__()

    def makeMessage(self) -> str:
        """
        Makes the message that gets sent to the recipients.
        :return: the message that gets sent to the recipients.
        """
        return f"{self.player} has spread some Honey at {self.location}!"

    def determineRecipients(self, **kwargs):
        """
        Determines the recipients for both pm and channels.
        """
        self.__determinepmrecipients()
        self._determinechannelrecipients()

    def __determinepmrecipients(self):
        """
        Determines the recipients for pm. If a user has configured that he wants a pm if honey gets spread at that
        location he gets a pm.
        """
        self._pmrecipients = list(PmConfig.objects.filter(event=self.EVENTNAME, data__location__iexact=self.location))
