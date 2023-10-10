from django.db import models
from django.db.models import UniqueConstraint

from api.basemodel import BaseModel


class EventconfigPermissions(BaseModel):
    guild = models.PositiveBigIntegerField()
    role = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["guild", "role"], name='unique_permissionconfig'),
        ]
