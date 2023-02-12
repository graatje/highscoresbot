import jsonschema


class Validators:
    LOGIN_SCHEMA = {
        "type": "object",
        "properties": {
            "data": {
                    "type": "object",
                    "properties": {
                            "username": {"type": "string"},
                            "password": {"type": "string"},
                    },
                "required": ["username", "password"],
                },

        },
        "required": ["data"],
    }
    EVENT_SCHEMA = {
        "type": "object",
        "properties": {
            "eventtype": {
                "enum": ['altar', 'altaramounts', 'chest', 'cwend', 'elite4', 'encounter', 'goldrush', 'honey', 'roll', 'swarm', 'tournament', 'worldboss', 'worldbosstime']
            },
        },
        "required": ["eventtype"],
        "allOf": [
            # altar
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "altar"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "player": {
                                    "type": "string",
                                },
                                "altartype": {
                                    "enum": ["Arceus", "Kyogre", "Diancie"],
                                },
                                "amount": {
                                    "type": "string",
                                }
                            },
                            "required": ["player", "altartype", "amount"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # altaramounts
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "altaramounts"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "amountarceus": {
                                    "type": "string",
                                },
                                "maxarceus": {
                                    "type": "string",
                                },
                                "amountkyogre": {
                                    "type": "string",
                                },
                                "maxkyogre": {
                                   "type": "string",
                                },
                                "amountdiancie": {
                                    "type": "string",
                                },
                                "maxdiancie": {
                                    "type": "string"
                                }
                            },
                            "required": ["amountarceus", "maxarceus", "amountkyogre", "maxkyogre", "amountdiancie", "maxdiancie"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # chest
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "chest"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "player": {
                                    "type": "string"
                                },
                                "location": {
                                    "type": "string"
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            },
                            "required": ["player", "location"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # cwend
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "cwend"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "tier": {
                                    "type": "number",
                                },
                                "firstplace": {
                                    "type": "string",
                                },
                                "bpfirstplace": {
                                    "type": "number",
                                },
                                "secondplace": {
                                    "type": "string",
                                },
                                "bpsecondplace": {
                                    "type": "number",
                                },
                                "thirdplace": {
                                    "type": "string",
                                },
                                "bpthirdplace": {
                                    "type": "number",
                                },
                                "bestplayer": {
                                    "type": "string",
                                },
                                "bestplayerwins": {
                                    "type": "number",
                                },
                                "bestplayerlosses": {
                                    "type": "number"
                                }
                            },
                            "required": ['tier', 'firstplace', 'bpfirstplace', 'secondplace', 'bpsecondplace', 'thirdplace', 'bpthirdplace', 'bestplayer', 'bestplayerwins', 'bestplayerlosses'],
                        },
                    },
                    "required": ["data"]
                }
            },
            # elite4
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "elite4"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "player": {
                                    "type": "string"
                                },
                                "region": {
                                    "enum": ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"]
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            },
                            "required": ["player", "region"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # encounter
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "encounter"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "player": {
                                    "type": "string",
                                },
                                "level": {
                                    "type": "number",
                                },
                                "pokemon": {
                                    "type": "string",
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            },
                            "required": ["player", "level", "pokemon"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # goldrush
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "goldrush"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string"
                                }
                            },
                            "required": ["location"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # honey
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "honey"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string"
                                }
                            },
                            "required": ["location"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # roll
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "roll"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "player": {
                                    "type": "string",
                                },
                                "level": {
                                    "type": "number",
                                },
                                "pokemon": {
                                    "type": "string",
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date"
                                }
                            },
                            "required": ["player", "level", "pokemon"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # swarm
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "swarm"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "pokemon1": {
                                    "type": "string",
                                },
                                "pokemon2": {
                                    "type": "string",
                                },
                                "location": {
                                    "type": "string",
                                }
                            },
                            "required": ["location", "pokemon1", "pokemon2"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # tournament
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "tournament"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "tournament": {
                                    "enum": ["Little Cup", "Self Caught", "Ubers", "Set Level 100", "Monotype"],
                                },
                                "minstillstart": {
                                    "type": "number",
                                },
                                "prizes": {
                                    "type": "string",
                                }
                            },
                            "required": ["tournament", "minstillstart", "prizes"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # worldboss
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "worldboss"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "pokemon": {
                                    "type": "string",
                                },
                                "location": {
                                    "type": "string",
                                },
                                "date": {
                                    "type": "string",
                                    "format": "date"
                                },
                            },
                            "required": ["location", "pokemon"],
                        },
                    },
                    "required": ["data"]
                }
            },
            # worldbosstime
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "swarm"
                        },
                    },
                    "required": ["eventtype"],
                },
                "then": {
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "hours": {
                                    "type": "string",
                                },
                                "minutes": {
                                    "type": "number",
                                },
                            },
                            "required": ["hours", "minutes"],
                        },
                    },
                    "required": ["data"]
                }
            },
        ],
    }

    @classmethod
    def validateJson(cls, actiontype, jsonData):
        if actiontype is None:
            raise jsonschema.ValidationError("'command' is a required property")

        # @todo replace with switch when moved to python 3.11
        if actiontype == "login":
            jsonschema.validate(instance=jsonData, schema=cls.LOGIN_SCHEMA)
        elif actiontype == "event":
            jsonschema.validate(instance=jsonData, schema=cls.EVENT_SCHEMA)
        return True


if __name__ == "__main__":
    Validators.validateJson('event', {
    "type": "event",
    "eventtype": "tournament",
    "data": {
        "tournament": "Monotype",
        "minstillstart": "30",
        "prizes": "PvP Token (250), Credit (400), 30 Day GM Ticket (1)"
    }
})
    #Validators.validateJson('event', {"type": "event", "eventtype": "goldrush", "data": {"location": "mt moon"}})