from django.db import models


class DefaultClanname(models.Model):
    guild = models.PositiveBigIntegerField(primary_key=True)
    clan = models.TextField()
