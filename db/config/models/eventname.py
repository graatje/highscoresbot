from django.db import models


class Eventname(models.Model):
    name = models.TextField(max_length=50, primary_key=True)
    fields = models.JSONField(default=dict)

    def __str__(self):
        return self.name
