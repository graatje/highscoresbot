from django.db import models


class Worldboss(models.Model):
    pokemon = models.TextField()
    date = models.DateField()
    participants = models.IntegerField(default=0)

    def to_json(self):
        return {
            "date": self.date,
            "pokemon": self.pokemon,
            "participants": self.participants
        }
