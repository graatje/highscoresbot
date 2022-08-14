from django.db import models


class Eventname(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name
