from ppobyter.ingame_commands.framework.ingamecommand import ingameCommand


@ingameCommand()
def getencounters(player: str):
    """
    gets the encounters of a player

    :param player: the player to get the encounters of
    """
    print(player)
    return ["i", "am", "a", "test"]


def register_commands(client):
    client.register_command(getencounters)
