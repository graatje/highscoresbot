from django.db import models
from django.db.models import UniqueConstraint

from api.ingame_data.models import Eventname


class PmConfig(models.Model):
    event = models.ForeignKey(Eventname, on_delete=models.PROTECT)
    user = models.PositiveBigIntegerField()
    data = models.JSONField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["event", "user", "data"], name='unique_pmevents'),
        ]

    def fetch_event(self):
        return self.event
