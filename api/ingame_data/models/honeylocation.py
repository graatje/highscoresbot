from django.db import models

from api.basemodel import BaseModel


class Honeylocation(BaseModel):
    location = models.TextField(max_length=80)
