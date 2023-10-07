from .event import Event
from ..main import Main


class Disconnect(Event):
    def __init__(self):
        self.EVENTNAME = "disconnect"
        super(Disconnect, self).__init__()

    def makeMessage(self) -> str:
        """
        makes the message to send to the recipients.
        :return: The message to send to the recipients
        """
        return "Client disconnected."

    def determineRecipients(self, **kwargs):
        """
        determines the recipients for the event.
        :param kwargs: none required
        """
        pass

    async def __call__(self, client: Main):
        owner = await client.fetch_owner()
        await owner.send(self.makeMessage())
