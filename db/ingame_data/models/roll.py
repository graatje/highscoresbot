from django.db import models


class Roll(models.Model):
    playername = models.TextField(max_length=50)
    pokemon = models.TextField(max_length=50)
    date = models.DateField()
    level = models.PositiveSmallIntegerField(null=True)

    def to_json(self):
        resp = {"playername": self.playername,
                "pokemon": self.pokemon,
                "date": self.date,
                "level": self.level}
        return resp
