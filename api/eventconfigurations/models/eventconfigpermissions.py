from django.db import models
from django.db.models import UniqueConstraint


class EventconfigPermissions(models.Model):
    guild = models.PositiveBigIntegerField()
    role = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["guild", "role"], name='unique_permissionconfig'),
        ]
