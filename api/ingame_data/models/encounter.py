import datetime

from django.db import models

from api.basemodel import BaseModel


class Encounter(BaseModel):
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

    def __str__(self):
        json = self.to_json()
        json["level"] = f"Lv {self.level}" if self.level else ""
        return "{player} has encountered a {level} {pokemon} on {date}".format(**json)
