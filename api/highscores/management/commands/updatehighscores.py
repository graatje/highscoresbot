import os
from abc import ABC
from django.core.management.base import BaseCommand

from api.highscores.management.commands._webscraper.highscoresupdater import HighscoresUpdater
from api.highscores.management.commands._webscraper.ppowebsession import PpoWebSession


class Command(BaseCommand, ABC):
    help = 'Updates the highscores with the highscoresconfig.'

    def handle(self, *args, **options):
        websession = PpoWebSession(os.environ.get('ppousername'), os.environ.get('ppopassword'))
        websession.login()
        highscores_updater = HighscoresUpdater(websession,
                                               timeout=int(os.environ.get("webscraperequestinterval", 5)),
                                               onerrortimeout=int(os.environ.get("onwebscrapeerrortimeout", 300))
                                               )
        highscores_updater.updateHighscores()
