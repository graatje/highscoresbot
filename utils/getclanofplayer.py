from api.highscores.models import Highscore


def getClanOfPlayer(playername):
    obj = Highscore.objects.filter(data__username__iexact=playername, data__clan__isnull=False).first()
    if obj:
        return obj.data['clan']
