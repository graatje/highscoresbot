from asgiref.sync import sync_to_async
from django.db import models


class BaseModel(models.Model):
    async def adelete(self):
        await sync_to_async(self.delete)()

    class Meta:
        abstract = True
