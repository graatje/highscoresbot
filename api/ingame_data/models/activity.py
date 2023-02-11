from django.db import models


class Activity(models.Model):
    player = models.TextField(max_length=50, primary_key=True)
    lastonline = models.DateTimeField()

    def __str__(self):
        return f"{self.playername} last online at: {self.lastonline}"

    def get_lastonline(self, obscurified=True):
        return self.lastonline.date() if obscurified else self.lastonline
