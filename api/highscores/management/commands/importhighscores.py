from abc import ABC
import json
from django.core.management.base import BaseCommand
from api.highscores.models import HighscoreConfig
import csv


class Command(BaseCommand, ABC):
    help = 'imports the highscores from a csv.'

    def handle(self, *args, **options):
        HighscoreConfig.objects.all().delete()
        with open("highscores.csv") as file:
            filereader = csv.reader(file)
            for row in filereader:
                HighscoreConfig(highscorename=row[0], url=row[1], pagesamount=row[2], fieldmapping=json.loads(row[3]), verbose_name=row[4], intfields=json.loads(row[5])).save()
