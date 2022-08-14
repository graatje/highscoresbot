from django.db import models


class HighscoreConfig(models.Model):
    highscorename = models.TextField(primary_key=True)
    url = models.URLField()
    pagesamount = models.PositiveSmallIntegerField()

    # the fieldname we give it and the fieldname it has in the website.
    # needed because it needs to be a valid variable name to be able to filter it.
    fieldmapping = models.JSONField()
    verbose_name = models.TextField(default="")

    def __str__(self):
        return self.highscorename
