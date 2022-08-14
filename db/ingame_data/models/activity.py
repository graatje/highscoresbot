from django.db import models


class Activity(models.Model):
    playername = models.TextField(max_length=50)
    lastonline = models.DateTimeField()

    def __str__(self):
        return f"{self.playername} lastonline at: {self.lastonline}"
