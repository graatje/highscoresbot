from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class Playerconfig(models.Model):
    guild = models.PositiveBigIntegerField()
    player = models.TextField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(Lower("player").desc(), "player", name='unique_playerconfig'),  # a player can be configured only once per guild
        ]
