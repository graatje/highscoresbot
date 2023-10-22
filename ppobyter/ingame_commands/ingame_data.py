from api.ingame_data.models import Encounter
from ppobyter.ingame_commands.framework.ingamecommand import ingameCommand
from django.core.paginator import Paginator


@ingameCommand()
def getencounters(player: str, page: int = 1):
    """
    gets the encounters of a player

    :param player: the player to get the encounters of
    :param page: the page to get the encounters of. Max 10 per page.
    """
    qs = list(Encounter.objects.filter(player__iexact=player).order_by("-date"))
    paginator = Paginator(qs, 10)
    values = paginator.page(page).object_list

    messages = [str(value) for value in values]
    return messages or ["No encounters found for this player."]

@ingameCommand()
def getpokemon(pokemon: str, page: int = 1):
    """
    gets the encounters of a pokemon

    :param pokemon: the pokemon to get the encounters of
    :param page: the page to get the encounters of. Max 10 per page.
    """
    qs = list(Encounter.objects.filter(pokemon__iexact=pokemon).order_by("-date"))
    paginator = Paginator(qs, 10)
    values = paginator.page(page).object_list

    messages = [str(value) for value in values]
    return messages or ["No encounters found for this pokemon."]

@ingameCommand()
def getdate(date: str, page: int = 1):
    """
    gets the encounters of a specific date

    :param date: the date to get the encounters of
    :param page: the page to get the encounters of. Max 10 per page.
    """
    qs = list(Encounter.objects.filter(date__iexact=date).order_by("player"))
    paginator = Paginator(qs, 10)
    values = paginator.page(page).object_list

    messages = [str(value) for value in values]
    return messages or ["No encounters found for this date."]


def register_commands(client):
    client.register_command(getencounters)
    client.register_command(getpokemon)
    client.register_command(getdate)
