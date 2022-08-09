from typing import Dict


class HighscoreConfig:
    def __init__(self, highscorename: str, pagesamount: int, url: str, fieldmapping: Dict[str, str]):
        self.highscorename = highscorename
        self.pagesamount = pagesamount
        self.fieldmapping = fieldmapping
        self.url = url

    def __eq__(self, other):
        if type(other) == type(self):
            return self.highscorename == other.highscorename

    def __str__(self):
        return self.highscorename
