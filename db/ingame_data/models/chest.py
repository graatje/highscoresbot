from django.db import models


class Chest(models.Model):
    playername = models.TextField(max_length=50)
    location = models.TextField(max_length=80)
    date = models.DateField()
