from api.ingame_data.models import Encounter
from ppobyter.ingame_commands.framework.ingamecommand import ingameCommand
from django.core.paginator import Paginator


@ingameCommand()
def getencounters(player: str, page: int=1):
    """
    gets the encounters of a player

    :param player: the player to get the encounters of
    :param page: the page to get the encounters of. Max 10 per page.
    """
    qs = list(Encounter.objects.filter(player__iexact=player).order_by("-date"))
    paginator = Paginator(qs, 10)
    values = paginator.page(page).object_list

    messages = []
    for value in values:
        message = "<"
        for key, val in value.to_json().items():
            message += f"<<{key}> : {val} >"
        message += ">"
        messages.append(message)
    return messages


def register_commands(client):
    client.register_command(getencounters)
