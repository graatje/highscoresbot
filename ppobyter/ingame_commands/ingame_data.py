from ppobyter.ingame_commands.framework.ingamecommand import ingameCommand


@ingameCommand()
def getencounters(player: str):
    """
    gets the encounters of a player

    :param player: the player to get the encounters of
    """
    pass


def register_commands(client):
    client.register_command(getencounters)
