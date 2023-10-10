from abc import ABC
from django.db.models import Q

from api.eventconfigurations.models import Clanconfig, Eventconfiguration, Playerconfig
from utils.getclanofplayer import getClanOfPlayer
from .event import Event


class ClanEvent(Event, ABC):
    """
    This is an event whose recipients are based on the clan of the player.
    """

    def __init__(self, player: str):
        """
        Calls the superclass and sets the player attribute.
        :param player: the player on whose clan the recipients are based.
        """
        self.player = player
        super(ClanEvent, self).__init__()

    def _determinechannelrecipients(self):
        """
        determines the channel recipients based on the players clan
        """
        if (clan := getClanOfPlayer(self.player)) is None:
            clan = 'all'

        clanconfigguilds = [clanconfig.guild for clanconfig in list(Clanconfig.objects.filter(Q(clan__iexact=clan) | Q(clan__iexact='all')).distinct('guild'))]

        playerconfigguilds = [playerconfig.guild for playerconfig in list(Playerconfig.objects.filter(player__iexact=self.player).distinct('guild'))]

        self._recipients = list(Eventconfiguration.objects.filter(eventname=self.EVENTNAME,
                                                                  guild__in=clanconfigguilds + playerconfigguilds,
                                                                  channel__isnull=False))
