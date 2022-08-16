from django.db import models


class Chest(models.Model):
    playername = models.TextField(max_length=50)
    location = models.TextField(max_length=80)
    date = models.DateField()

    def to_json(self):
        return {
            "playername": self.playername,
            "location": self.location,
            "date": self.date
        }
