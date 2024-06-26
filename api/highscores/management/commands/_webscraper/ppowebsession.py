import time
from typing import Tuple
import lxml
import requests
from lxml import html
import re
from bs4 import BeautifulSoup, SoupStrainer
from requests import Session, Response


class PpoWebSession:
    def __init__(self, username: str, password: str, interval: int = 5):
        # @todo handle connection issues and raise more specific errors.
        """
        initializes cookies and interval.
        :param username: pokemon planet username
        :param password: pokemon planet password
        :param interval: interval after pages are loaded.
        """
        self.__cookies = {"user": username, "passwrd": password, "cookielength": "-1"}
        self.interval = interval
        self.session: Session = None

    def login(self):
        try:
            self.loginmethod1()
        except Exception as e:
            print(e)
            self.loginmethod2()

    def getpage(self, page: str) -> str:
        """
        gets the html of the webpage.
        :param page: the url to get.
        :return: the html of the provided webpage.
        """
        if self.session is not None:
            response: Response = self.session.get(page)
            time.sleep(self.interval)  # @todo why here???????????
            return response.text
        else:
            raise Exception("logged out!")

    def loginmethod1(self):
        """
        Logging in to the pokemon planet website to be able to visit the highscore pages.
        """
        if self.session is not None:
            self.session.close()
        self.session = requests.session()
        r = self.session.post("https://pokemon-planet.com/")
        hiddencookies = self.__gethiddeninput(r.content)
        logincookies = self.__cookies.copy()
        logincookies[hiddencookies[0]] = hiddencookies[1]

        self.session.post("https://pokemon-planet.com/forums/index.php?action=login2", data=logincookies)

        self.session.post("https://pokemon-planet.com/forums/index.php?action=login2;sa=check;member=" +
                          self.__getuserid())

    def logout(self):
        """
        closing the web session, and logging out.
        """
        response = self.session.post("https://pokemon-planet.com/forums/index.php")
        for link in BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                if "https://pokemon-planet.com/forums/index.php?action=logout;sesc=" in link["href"]:
                    self.session.post(link["href"])
                    self.session.close()
                    self.session = None
                    print("logged out!")
                    break
        else:
            print("not logged out.")

    def __getuserid(self) -> str:
        """
        gets the userid.
        :return: the user id
        """
        userid = self.session.get("https://pokemon-planet.com/getUserInfo.php")
        if userid.status_code == 200:
            match = re.search(r"(?<=id=)([0-9]+?)(?=&)", userid.text)
            if match:
                return match.group()
            raise Exception("unable to get the userid.\n" + userid.text)
        raise Exception(f"status code {userid.status_code} returned!")

    def __gethiddeninput(self, pagecontent: bytes) -> Tuple[str, str]:
        """
        gets the hidden input of the ppo page.
        :param pagecontent: the html of the page as bytes.
        :return: name, value of the hidden input.
        """
        tree = html.fromstring(pagecontent)
        element: lxml.html.InputElement = tree.xpath("/html/body/div[8]/div/div/div[2]/div/div[1]/div/form/div[2]/input[3]")[0]
        return element.name, element.value

    def loginmethod2(self):
        if self.session is not None:
            self.session.close()
        self.session = requests.session()
        req = self.session.get(r"https://pokemon-planet.com/forums/index.php?topic=18395.0")
        tree = html.fromstring(req.content)
        element = lxml.html.InputElement = tree.xpath("/html/body/div[3]/div/form/div/div[3]/input")[0]
        logincookies = self.__cookies.copy()
        logincookies[element.name] = element.value
        self.session.post("https://pokemon-planet.com/forums/index.php?action=login2", data=logincookies)

if __name__ == "__main__":
  #   session = PpoWebSession("username", "password")
  # #  help(session)
  #   session.login()
    import pandas
    session = PpoWebSession()  # username, password
    session.login()
    theresult = session.getpage("https://pokemon-planet.com/topStrongestClans.php")
    dataframe = pandas.read_html(theresult)
    df = dataframe[-1]
    writer = pandas.ExcelWriter('test.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    for index, row in df.iterrows():
        if index == 0:  # this is just the layout of the table.
            continue
        elif index == 1:
            print(list(row.values))
        else:
            print(row.values)
