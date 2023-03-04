from django.db import models
import datetime


class Chest(models.Model):
    player = models.TextField(max_length=50)
    location = models.TextField(max_length=80)
    date = models.DateField(default=datetime.date.today)

    def to_json(self):
        return {
            "playername": self.player,
            "location": self.location,
            "date": self.date
        }
