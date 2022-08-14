from django.db import models
from django.db.models import UniqueConstraint


class Clanconfig(models.Model):
    guild = models.PositiveBigIntegerField()
    clan = models.TextField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["guild", "clan"], name='unique_clanconfig'),  # a clan can be configured only once per guild
        ]
