import discord
from typing import Union, List
from api.eventconfigurations.models import Eventconfiguration, PmConfig


class Event:
    """
    This is the baseclass of an event. It can determine channelrecipients based on the eventname provided.
    When you call this class the event will be sent.
    """
    def __init__(self):
        """
        Here pingroles, recipients, alivetime and pmrecipients are initialized.
        It also calls the determineRecipients method.
        """
        self.EVENTNAME: str
        self._recipients: List[Eventconfiguration] = []
        self._pmrecipients = []
        self.determineRecipients()

    def determineRecipients(self, **kwargs):
        """
        Here pingroles, recipients, alivetime and pmrecipients are determined. This method should be overridden.
        :param kwargs:
        :raise NotImplementedError if it's not implemented.
        """
        raise NotImplementedError

    def _determinechannelrecipients(self):
        """
        Base method for determining channel recipients based on eventname.
        :return:
        """
        self._recipients = list(Eventconfiguration.objects.filter(channel__isnull=False, eventname=self.EVENTNAME))
        print(self._recipients)

    def makeMessage(self) -> Union[str, discord.Embed]:
        """
        Here the message that must be sent gets made.
        :return: either a discord embed or a string that must be sent.
        :raises NotImplementedError if this method is not implemented in the subclass.
        """
        raise NotImplementedError

    async def __call__(self, client: discord.client.Client):
        """
        send the event to all recipients.
        :param client, the discord client
        """
        for configuration in self._recipients:
            try:
                chan = await client.fetch_channel(configuration.channel)
                msg = self.makeMessage()
                if configuration.pingrole is not None and type(msg) != discord.Embed:
                    msg += f"<@&{configuration.pingrole}>"

                if type(msg) == discord.embeds.Embed:
                    await chan.send(embed=msg, delete_after=configuration.time_in_channel * 60 if configuration.time_in_channel else configuration.time_in_channel)
                else:
                    await chan.send(msg, delete_after=configuration.time_in_channel * 60 if configuration.time_in_channel else configuration.time_in_channel)
            except Exception as e:
                print(e, configuration)

        for pmconfig in self._pmrecipients:
            try:
                user = await client.fetch_user(pmconfig.user)
                await user.send(self.makeMessage())
            except Exception as e:
                # probably 403 forbidden exceptions etc, those exceptions will be catched and ignored in the future.
                print(e)
