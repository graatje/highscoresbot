import os
from typing import List



import log
from config import Config
from ppowebsession import PpoWebSession
import requests
from highscoreconfig import HighscoreConfig
import time
from dotenv import load_dotenv
import pandas
load_dotenv(dotenv_path=Config.root_folder + "/.env")  # we need those envs before the singleton has been made.

from highscoresbotapi import HighscoresbotAPI


logger = log.Logger()
logger.setLevel(50)


class HighscoresUpdater:
    """
    steps:
    1. get the available highscores and their configurations via the API.
    """
    def __init__(self, websession: PpoWebSession, timeout=600):
        self.__ppowebsession: PpoWebSession = websession
        self.__timeout = timeout
        self.__configurations: List[HighscoreConfig] = []
        self.__loadConfigurations()

    def main(self):
        while True:
            for config in self.__configurations:
                self.updateHighscore(config)

    def updateHighscore(self, config: HighscoreConfig):
        for page in range(1, config.pagesamount + 1):

            self.__updateHighscorePage(config, page)

            time.sleep(self.__timeout)

    def __updateHighscorePage(self, config: HighscoreConfig, page):

        html = self.__ppowebsession.getpage(config.url + f"?page={page}")

        df = pandas.read_html(html)[0]
        mapping = {}
        alldata = []
        try:
            for i, row in df.iterrows():
                if i == 0:
                    row = [val.lower() for val in list(row)]
                    for index, (key, value) in enumerate(config.fieldmapping.items()):
                        mapping[key] = row.index(value)
                    mapping["rank"] = row.index("rank")
                    continue  # skipping the layout.
                data = {"data": {}}
                for key, index in mapping.items():
                    if key.lower() == "rank":
                        data["rank"] = row[index]
                    elif isinstance(row[index], str) or isinstance(row[index], int):
                        data["data"][key] = row[index]
                    else:
                        data["data"][key] = ""
                alldata.append(data)

            resp = HighscoresbotAPI().makePatchRequest(Config.api_root + "highscores/highscore/" + config.highscorename + "/",
                                                       json=alldata)
            if not resp:
                logger.warning(f"the server responded with status code {resp.status_code} and json {resp.json()}")
        except Exception as e:
            logger.exception("exception during highscore " + config.highscorename)

    def __loadConfigurations(self, hardReload: bool = False):
        """

        :param hardReload: should existing configurations be removed before loading in new ones?
        :return:
        """
        if hardReload:
            self.__configurations = []
        resp = requests.get(Config.api_root + "highscores/highscoreconfig/")
        if not resp:  # status code not ok
            logger.warning(f"loading configurations returned status code {resp.status_code}. "
                           f"json returned: {resp.json()}")
            return

        jsonresp = resp.json()
        for conf in jsonresp:
            try:
                highscoreconfig = HighscoreConfig(highscorename=conf["highscorename"],
                                                  url=conf["url"],
                                                  pagesamount=conf["pagesamount"],
                                                  fieldmapping=conf["fieldmapping"]
                                                  )
                if highscoreconfig not in self.__configurations:
                    self.__configurations.append(highscoreconfig)
                    logger.debug(f"added highscore configuration {highscoreconfig}")
            except Exception as e:
                logger.exception(f"error when loading a highscore configuration. JSON was: {str(conf)}")


if __name__ == "__main__":
    websession = PpoWebSession(username=os.environ.get("ppousername"), password=os.environ.get("ppopassword"))
    websession.login()
    HighscoresUpdater(websession=websession, timeout=5).main()
