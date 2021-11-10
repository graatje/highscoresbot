from highscores.highscore import Highscore


class Btwins(Highscore):
    def __init__(self):
        self.LAYOUT = ["Rank", "Username", "Wins", "Win Streak"]
        self.NAME = "btwins"
        self.LINK = "https://pokemon-planet.com/btWins.php"
        self.CREATEQUERY = "CREATE TABLE IF NOT EXISTS btwins(rank INTEGER PRIMARY KEY, name TEXT, wins TEXT, " \
                           "streak TEXT)"
        super(Btwins, self).__init__()

    def updatequery(self) -> str:
        return "UPDATE btwins SET name=?, wins=?, streak=? WHERE rank=?"

    def create(self, databasepath: str):
        """
        This method is to create the database and initialize the rank column.
        Calls the method from the superclass to set the amount of values to have when filling the database to 100
        instead of the default 1000.
        :param databasepath:
        """
        super()._create(databasepath, 100)
