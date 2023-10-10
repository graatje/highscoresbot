from django.db import models

from api.basemodel import BaseModel


class DefaultClanname(BaseModel):
    guild = models.PositiveBigIntegerField(primary_key=True)
    clan = models.TextField()
