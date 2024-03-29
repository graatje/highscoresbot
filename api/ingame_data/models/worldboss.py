from django.db import models

from api.basemodel import BaseModel


class Worldboss(BaseModel):
    pokemon = models.TextField()
    location = models.TextField()
    date = models.DateField(auto_now=True)
    participants = models.IntegerField(default=0)

    def to_json(self):
        return {
            "date": self.date,
            "pokemon": self.pokemon,
            "location": self.location,
            "participants": self.participants
        }
