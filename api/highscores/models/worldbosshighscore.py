from django.db import models

from api.ingame_data.models import Worldboss


class WorldbossHighscore(models.Model):
    worldboss = models.ForeignKey(Worldboss, on_delete=models.PROTECT)
    player = models.TextField()
    damage = models.PositiveIntegerField()
    rank = models.PositiveSmallIntegerField()

    def to_json(self):
        return {
            "player": self.player,
            "damage": self.damage,
            "rank": self.rank
        }

    def get_worldboss(self):
        return self.worldboss