from api.basemodel import BaseModel
from django.db import models
from api.ingame_data.models import Eventname


class Event(BaseModel):
    eventname = models.ForeignKey(Eventname, on_delete=models.PROTECT)
    data = models.JSONField(default=dict)
    time = models.DateTimeField()
