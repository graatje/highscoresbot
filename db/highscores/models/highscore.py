from django.db import models
from django.db.models import UniqueConstraint

from db.highscores.models.highscoreconfig import HighscoreConfig


class Highscore(models.Model):
    rank = models.IntegerField()
    highscore = models.ForeignKey(HighscoreConfig, on_delete=models.PROTECT)
    data = models.JSONField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["rank", "highscore"], name='unique_highscoreranks'),
        ]
