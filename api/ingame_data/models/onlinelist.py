from django.db import models

from api.basemodel import BaseModel


class Onlinelist(BaseModel):
    time = models.DateTimeField()
    onlineAmount = models.PositiveSmallIntegerField()
