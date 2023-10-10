from django.db import models

from api.basemodel import BaseModel


class Tournamentprize(BaseModel):
    prize = models.TextField(max_length=80)

    def __str__(self):
        return self.prize
