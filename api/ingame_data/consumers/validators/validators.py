import jsonschema


class Validators:
    LOGIN_SCHEMA = {
        "type": "object",
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
        },
        "required": ["username", "password"],
    }

    @classmethod
    def validateJson(cls, actiontype, jsonData):
        if actiontype is None:
            raise jsonschema.ValidationError("'type' is a required property")
        if actiontype == "login":
            jsonschema.validate(instance=jsonData, schema=cls.LOGIN_SCHEMA)

        return True


if __name__ == "__main__":
    Validators.validateJson('login', {'username': 'kevin'})
