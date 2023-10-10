from django.db import models
from django.db.models import UniqueConstraint

from api.basemodel import BaseModel


class Playerconfig(BaseModel):
    guild = models.PositiveBigIntegerField()
    player = models.TextField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(name='unique_playerconfig', fields=["player", "guild"]),  # a player can be configured only once per guild
        ]

