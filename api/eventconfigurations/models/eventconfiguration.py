from django.db import models
from django.db.models import UniqueConstraint

from api.ingame_data.models import Eventname


class Eventconfiguration(models.Model):

    eventname = models.ForeignKey(Eventname, on_delete=models.PROTECT)
    guild = models.PositiveBigIntegerField()
    channel = models.PositiveBigIntegerField(null=True)
    pingrole = models.PositiveBigIntegerField(null=True)
    time_in_channel = models.PositiveSmallIntegerField(null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["guild", "eventname"], name='unique_events'),  # one eventannouncement per guild
        ]

    def get_eventname(self):
        return str(self.eventname)
