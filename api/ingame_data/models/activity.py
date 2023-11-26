from django.db import models

from api.basemodel import BaseModel


class Activity(BaseModel):
    player = models.TextField(max_length=50, primary_key=True)
    lastonline = models.DateTimeField()

    def __str__(self):
        return f"{self.player} last online at: {self.lastonline}"

    def get_lastonline(self, obscurified=True):
        return self.lastonline.date() if obscurified else self.lastonline

    def to_dict(self, obscurified=True):
        return {
            "player": self.player,
            "lastonline": self.get_lastonline(obscurified)
        }
