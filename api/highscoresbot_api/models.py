from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    prefix = models.CharField(max_length=1, null=True, default=None)
