To add an ingame command, take the following steps:

1. You first start a websocket connection to the server.
2. Log in with the following message:
```json
{
    "command": "login",
    "data": {
        "username": "username",
        "password": "password"
    }
}
```
_haven't got an account? Message kevin123456 on discord_

3. Register the command to the server:

```json
{
    "command": "registercommand",
    "data": {
        "name": "testcommand",
        "description": "testcommand description",
        "commandarguments": [
            {
                "name": "testargument",
                "description": "testargument description",
                "required": true,
                "type": "string"
            },
            {
                "name": "testargument2",
                "description": "testargument description2",
                "required": true,
                "type": "number"
            }
        ]
    }
}
```

4. You now receive commands from the server in the following format:

```json
{
    "command": "command",
    "data": {
        "uid": "the unique id of the command",
        "command": "name of the commnand",
        "arguments": {
            "testargument": "the mapping you made in the registercommand message"
        },
        "user_id": your own user id,
        "expires_at": After this time the command will not be sent to the user anymore,
        "messages_remaining": amount of messages the user can send to the server. 
    }
}
```
example:
```json
{
    "command": "command",
    "data": {
        "uid": "lnxppgesglsz3xtt7li",
        "command": "testcommand",
        "arguments": {
            "testargument": "dd"
        },
        "user_id": 2,
        "expires_at": 1697752121620,
        "messages_remaining": 5
    }
}
```
Worth mentioning here is that if the user provided more arguments than there are present, then the remaining part will be added to the string of the last command. So if the user provided 3 arguments, but there are only 2, then the last argument will be added to the string of the last argument with a space in between.

6. You can now send a response to the server with the received uid from the server:
```json
{
    "command": "commandresponse",
    "data": {
        "uid": "lnxppgesglsz3xtt7li",
        "messages": ["testresponse that will be sent to ingame."]
    }
}
```
While messages_remaining is above 0, the user can send more messages to the server with the same uid if it is still within the timeout.