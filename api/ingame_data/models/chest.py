from django.db import models


class Chest(models.Model):
    player = models.TextField(max_length=50)
    location = models.TextField(max_length=80)
    date = models.DateField(auto_now=True)

    def to_json(self):
        return {
            "playername": self.player,
            "location": self.location,
            "date": self.date
        }
