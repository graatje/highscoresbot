from asgiref.sync import sync_to_async
from django.db import models
from django.db.models import UniqueConstraint

from api.basemodel import BaseModel
from api.ingame_data.models import Eventname


class Eventconfiguration(BaseModel):

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
