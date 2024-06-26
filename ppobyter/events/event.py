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
                await self.__handle_send(configuration, client)
            except (discord.errors.Forbidden, discord.errors.NotFound):
                await self.__handle_failed_send(configuration, client)
            except Exception as e:
                print(e, configuration)

        # for pmconfig in self._pmrecipients:
        #     try:
        #         user = await client.fetch_user(pmconfig.user)
        #         await user.send(self.makeMessage())
        #     except Exception as e:
        #         # probably 403 forbidden exceptions etc, those exceptions will be catched and ignored in the future.
        #         print(e)

    async def __handle_send(self, configuration, client: discord.Client):
        chan = await client.fetch_channel(configuration.channel)
        msg = self.makeMessage()

        if type(msg) != list:
            msg = [msg]

        pingSent = False
        for msg_part in msg:
            pingrole = configuration.pingrole if configuration.pingrole and not pingSent and type(msg_part) == str else None
            await self.__send_message(msg_part, configuration, chan, pingrole)

            pingSent = bool(pingrole)

        if configuration.failed_sends > 0:
            configuration.failed_sends = 0
            await configuration.asave()

    async def __send_message(self, msg, configuration, channel, pingrole=None):
        arguments = {
            "delete_after": configuration.time_in_channel * 60 if configuration.time_in_channel else None
        }
        if type(msg) == discord.embeds.Embed:
            arguments["embed"] = msg
        else:
            msg += f"<@&{pingrole}>" if pingrole else ""
            arguments["content"] = msg
        await channel.send(**arguments)

    async def __handle_failed_send(self, configuration, client):
        try:
            configuration.failed_sends += 1
            if configuration.failed_sends <= 20:
                await configuration.asave()
                return

            configuration.channel = None
            configuration.failed_sends = 0
            await configuration.asave()
            print(f"removed channel from eventconfiguration because of too many failed sends.")

            guild = await client.fetch_guild(configuration.guild)
            print("guild", guild)
            if not guild:
                return

            owner = await client.fetch_user(guild.owner_id)
            print("owner", owner)
            if not owner:
                return

            message = f"""
    I lack permissions to send messages in <#{configuration.channel}> in {guild.name}!
    Therefore i removed that channel from the eventconfiguration.
    Please give me permissions to send messages in there and reconfigure the eventconfiguration for the {configuration.eventname} event.
            """

            await owner.send(message)
        except Exception as e:
            print(e)
