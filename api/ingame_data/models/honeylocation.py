from django.db import models


class Honeylocation(models.Model):
    location = models.TextField(max_length=80)
