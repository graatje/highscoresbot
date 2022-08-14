from django.db import models


class Encounter(models.Model):
    playername = models.TextField(max_length=50)
    pokemon = models.TextField(max_length=50)
    date = models.DateField()
    level = models.PositiveSmallIntegerField(null=True)
