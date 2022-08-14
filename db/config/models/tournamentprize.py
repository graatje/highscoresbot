from django.db import models


class Tournamentprize(models.Model):
    prize = models.TextField(max_length=80)

    def __str__(self):
        return self.prize
