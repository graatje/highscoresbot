from django.db import models

from api.basemodel import BaseModel


class Eventname(BaseModel):
    name = models.TextField(max_length=50, primary_key=True)
    fields = models.JSONField(default=dict)

    def __str__(self):
        return self.name
