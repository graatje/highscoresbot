from django.db import models


class Worldbosslocation(models.Model):
    location = models.TextField(max_length=80)
    