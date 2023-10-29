from .clanevent import ClanEvent


class Chest(ClanEvent):
    """
    This is an event that happens when opening a treasure chest.
    """
    def __init__(self, player: str, location: str):
        self.location = location
        self.EVENTNAME = "chest"
        super(Chest, self).__init__(player)

    def determineRecipients(self):
        """
        Here the channelrecipients are determined.
        """
        self._determinechannelrecipients()

    def makeMessage(self) -> str:
        """
        Make the message that gets sent to the recipients.
        :return: The message that will get sent.
        """
        return f"{self.player} has opened a treasure chest at {self.location}!"
