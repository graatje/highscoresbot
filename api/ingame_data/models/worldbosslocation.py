from django.db import models

from api.basemodel import BaseModel


class Worldbosslocation(BaseModel):
    location = models.TextField(max_length=80)
    