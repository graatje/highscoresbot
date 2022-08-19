from django.db import models


class Worldboss(models.Model):
    pokemon = models.TextField()
    date = models.DateField()
