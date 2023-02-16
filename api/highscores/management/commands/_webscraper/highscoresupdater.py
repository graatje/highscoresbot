import log
from utils.utils import strip_characters

import time
import pandas
from api.highscores.management.commands._webscraper.ppowebsession import PpoWebSession
from api.highscores.models import HighscoreConfig, Highscore


logger = log.Logger(name="highscoresupdater")


class HighscoresUpdater:
    """
    steps:
    1. get the available highscores and their configurations via the API.
    """
    def __init__(self, websession: PpoWebSession, timeout=5):
        self.__ppowebsession: PpoWebSession = websession
        self.__timeout = timeout

    def updateHighscores(self):
        while True:
            for config in HighscoreConfig.objects.all():
                self.updateHighscore(config)

    def updateHighscore(self, config: HighscoreConfig):
        try:
            for page in range(1, config.pagesamount + 1):

                self.__updateHighscorePage(config, page)

                time.sleep(self.__timeout)
            logger.info(f"updated highscore {config.verbose_name}")
        except Exception as e:
            logger.warning(f"error updating highscore {config.verbose_name}")
            logger.exception(e)

    def __updateHighscorePage(self, config: HighscoreConfig, page):
        inverted_fieldmapping = {v: k for k, v in config.fieldmapping.items()}
        html = self.__ppowebsession.getpage(config.url + f"?page={page}")

        df = pandas.read_html(html)[0]
        rankindex = -1
        layout = []

        createdobjs = []
        updatedobjs = []
        for i, row in df.iterrows():
            row = [i if type(i) == str else '' for i in list(row)]
            if i == 0:

                layout = [inverted_fieldmapping.get(key, 'rank') for key in row]
                rankindex = row.index('Rank')
                continue
            obj, created = Highscore.objects.update_or_create(rank=int(row[rankindex]),
                                                              highscore=config,
                                                              defaults={"data": {layout[columnindex]: strip_characters(row[columnindex]) if config.intfields[layout[columnindex]] else row[columnindex] for columnindex in range(len(row))}})
            createdobjs.append(obj) if created else updatedobjs.append(obj)

        if updatedobjs:
            Highscore.objects.bulk_update(updatedobjs, ['data'])
        if createdobjs:
            Highscore.objects.bulk_create(createdobjs)
