from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    prefix = models.CharField(max_length=1, null=True, default=None)


class IngameCommand(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=100)
    commandarguments = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'user',),)

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "commandarguments": self.commandarguments,
            "user_id": self.user.id,
            "prefix": self.user.prefix
        }
