import sqlite3
from typing import List
import pandas


from commands.utils.utils import replacenan
from highscoresupdater.ppowebsession import PpoWebSession


class Highscore:
    def __init__(self, name, link, layout, createquery=None):
        """
        checks if a subclass has overridden the right attributes.
        """
        self.LINK: str = link
        self.LAYOUT: List[str] = layout
        self.NAME: str = name
        self.CREATEQUERY: str = createquery

    def getDbValues(self, query=None, clan=None, params: List = []):
        conn = sqlite3.connect(PathManager().getpath("highscores.db"))
        cur = conn.cursor()
        if query is not None:
            if clan is None:
                cur.execute(query, params)
            else:
                cur.execute(query, [clan] + params)
        elif query is None and clan is not None:
            cur.execute(f"SELECT * FROM {self.NAME} WHERE clan=?", (clan,))
        else:
            cur.execute(f"SELECT * FROM {self.NAME}")
        result = list(cur.fetchall())
        return result

    def create(self, databasepath: str):
        """
        This method is to create the database and initialize the rank column.
        :param databasepath:
        :param amount: the amount of values to put in the database.
        :return:
        """
        self._create(databasepath)

    def _create(self, databasepath, amount=1000):
        conn = sqlite3.connect(databasepath)
        cur = conn.cursor()
        cur.execute(self.CREATEQUERY)
        for i in range(1, amount + 1):
            try:
                cur.execute(f"INSERT INTO {self.NAME}(rank) VALUES(?)", (i,))
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()

    def updatequery(self) -> str:
        """
        This gives the query that should be called on update. Query should always have 'WHERE rank=?' as end.
        :return: the query that's needed to update the table.
        """
        raise NotImplementedError("No update query overridden.")

    def updatetable(self, ppowebsession: PpoWebSession):
        """
        updates the entire highscore.
        :param ppowebsession: logged in ppo web session.
        """
        for row in self.getValues(ppowebsession):
            self.insert(row)

    def getValues(self, ppowebsession: PpoWebSession) -> List[str]:
        """
        Gets all available pages of the highscore on the website and yields the highscores rows.
        :param ppowebsession:
        :return: a row with values.
        """
        old = 0  # the first rank value on the page.
        running = True
        page = 1
        while running:
            html = ppowebsession.getpage(self.LINK + f"?page={str(page)}")
            page += 1
            df_list = pandas.read_html(html)
            df = df_list[-1]
            for index, row in df.iterrows():
                if index == 0:  # this is just the layout of the table.
                    continue
                elif index == 1:
                    if row[0] == old:  # check if the rank is updating, if its not, we reached the end of the highscore.
                        running = False
                        break
                    old = row[0]
                yield list(row.values)

    def insert(self, values: List[str]):
        """
        Inserts the values into the database. replaces nan values with empty string.
        :param values:
        """
        query = self.updatequery()
        values = replacenan(values, "")
        values = [str(val).lower() for val in values]
        if len(values) != query.count("?"):
            raise ValueError(f"length not equal!\nquery: {query}\nValues: {str(values)}")
        conn = sqlite3.connect(PathManager().getpath("highscores.db"))
        cur = conn.cursor()
        cur.execute(query, values[1:] + [int(values[0])])  # rank as last.
        conn.commit()
        conn.close()


if __name__ == "__main__":
    Highscore()
