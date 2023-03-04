import datetime

from django.db import models


class Roll(models.Model):
    player = models.TextField(max_length=50)
    pokemon = models.TextField(max_length=50)
    date = models.DateField(default=datetime.date.today)
    level = models.PositiveSmallIntegerField(null=True)

    def to_json(self):
        resp = {"player": self.player,
                "pokemon": self.pokemon,
                "date": self.date,
                "level": self.level}
        return resp
