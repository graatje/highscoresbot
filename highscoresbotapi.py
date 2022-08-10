import os
import time

import requests
import jwt
from requests import Response

import log
from config import Config

logger = log.Logger()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class HighscoresbotAPI(metaclass=Singleton):
    def __init__(self, username=None, password=None):
        print("instance of highscoresbotapi made.")
        if username is None or password is None:
            raise ValueError("this can only be used if a singleton instance has already been made.")
        self.__accesstoken = None
        self.__username = username
        self.__password = password
        self.__refreshtoken = None
        self.__expiration = 0

    def getToken(self):
        if self.__refreshtoken is not None:
            resp = requests.post(Config.api_root + "token/refresh/", json={"refresh": self.__refreshtoken})
            self.__refreshtoken = None
            respjson = resp.json()
            if resp:
                self.__accesstoken = respjson["access"]
            else:
                logger.warning(f"error when getting access token via refresh token. "
                               f"api returned status code {resp.status_code} with json {respjson}")
        else:
            resp = requests.post(Config.api_root + "token/",
                                 json={"username": self.__username, "password": self.__password})
            respjson = resp.json()
            if resp:
                self.__refreshtoken = respjson["refresh"]
                self.__accesstoken = respjson["access"]
            else:
                logger.warning(f"error when logging in. "
                               f"api returned status code {resp.status_code} with json {respjson}")
        if self.__accesstoken is not None:
            algorithm = jwt.get_unverified_header(self.__accesstoken)["alg"]
            decoded = jwt.decode(self.__accesstoken, algorithms=[algorithm], options={"verify_signature": False})
            self.__expiration = decoded["exp"]
        else:
            logger.warning("NO ACCESS TOKEN OBTAINED!!")

    def ensureToken(self):
        if time.time() > self.__expiration - 5:
            self.getToken()

    def makePostRequest(self, url, json=None, **kwargs) -> Response:
        self.ensureToken()
        headers = {"Authorization": f"Bearer {self.__accesstoken}"}
        return requests.post(url, headers=headers, json=json, **kwargs)

    def makeGetRequest(self, url, params=None, **kwargs):
        self.ensureToken()
        headers = {"Authorization": f"Bearer {self.__accesstoken}"}
        return requests.get(url, headers=headers, params=params, **kwargs)

    def makePatchRequest(self, url, json=None, **kwargs):
        self.ensureToken()
        headers = {"Authorization": f"Bearer {self.__accesstoken}"}
        return requests.patch(url, headers=headers, json=json, **kwargs)

    def makePutRequest(self, url, json=None, **kwargs):
        self.ensureToken()
        headers = {"Authorization": f"Bearer {self.__accesstoken}"}
        return requests.put(url, headers=headers, json=json, **kwargs)

    def makeDeleteRequest(self, url, **kwargs):
        self.ensureToken()
        headers = {"Authorization": f"Bearer {self.__accesstoken}"}
        return requests.delete(url, headers=headers, **kwargs)


instance = HighscoresbotAPI(os.environ.get("apiusername"), os.environ.get("apipassword"))
