from docstring_parser.rest import parse


class IngameCommand:
    def __init__(self, name, description, aliases, arguments, execute):
        self.name = name
        self.description = description
        self.aliases = aliases
        self.arguments = arguments
        self.execute = execute

    def __call__(self, *args, **kwargs):
        print(args, kwargs)
        print(self.execute.__code__.co_varnames)
        return self.execute(*args, **kwargs)

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "aliases": self.aliases,
            "commandarguments": self.arguments
        }


def ingameCommand(name=None, description=None, aliases=()):
    def decorator(command):
        parseddoc = parse(command.__doc__)
        # validating function docstring
        if not parseddoc.short_description:
            raise ValueError("missing description of this command.")


        # Parsing params
        params = {param.arg_name: param for param in parseddoc.params if param.arg_name}
        arguments = []

        varnames = command.__code__.co_varnames[:command.__code__.co_argcount]
        for i, arg in enumerate(varnames):
            # validating command arguments
            if arg not in command.__annotations__:
                raise ValueError(f"missing annotation for argument {arg}.")
            if params[arg].description is None:
                raise ValueError(f"missing description for argument {arg}.")
            arguments.append({
                "name": arg,
                "description": params[arg].description,
                "required": len(varnames) - len(command.__defaults__) >= i + 1,
                "type": "number" if command.__annotations__[arg] == int else "string"
            })

        return IngameCommand(name=name or command.__name__,
                             description=description or (parseddoc.short_description + " --- " + (parseddoc.long_description or "")).replace("\n", " --- "),
                             aliases=aliases,
                             arguments=arguments,
                             execute=command)
    return decorator
