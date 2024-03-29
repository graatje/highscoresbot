from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from api.basemodel import BaseModel


class Clanconfig(BaseModel):
    guild = models.PositiveBigIntegerField()
    clan = models.TextField(max_length=200)

    class Meta:
        constraints = [
            UniqueConstraint(Lower("clan").desc(), "guild", name='unique_clanconfig'),  # a clan can be configured only once per guild
        ]
