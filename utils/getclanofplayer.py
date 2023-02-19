from api.highscores.models import Highscore


def getClanOfPlayer(playername):
    return Highscore.objects.filter(data__username__iexact=playername, data__clan__isnull=False).first().data['clan']
