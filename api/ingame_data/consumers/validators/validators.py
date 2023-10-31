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
            "data": {
                "type": "object",
                "properties": {
                    "eventtype": {
                        "enum": ['altar', 'altaramounts', 'chest', 'cwend', 'elite4', 'encounter', 'goldrush', 'honey', 'itembomb', 'roll', 'swarm', 'tournament', 'worldboss', 'worldbosstime']
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
            # itembomb
            {
                "if": {
                    "properties": {
                        "eventtype": {
                            "const": "itembomb"
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
                                    "item": {
                                        "type": "string",
                                    },
                                },
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
                            "const": "worldbosstime"
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
        }
    }

    REGISTERCOMMAND_SCHEMA = {
       "type": "object",
       "properties": {
          "data": {
             "type": "object",
             "properties": {
                "name": {
                   "type": "string"
                },
                "description": {
                   "type": "string"
                },
                "commandarguments": {
                   "type": "array",
                   "items": {
                      "type": "object",
                      "properties": {
                         "name": {
                            "type": "string"
                         },
                         "description": {
                            "type": "string"
                         },
                         "required": {
                            "type": "boolean"
                         },
                         "type": {
                            "enum": [
                               "string",
                               "number"
                            ]
                         }
                      },
                      "required": [
                          "name",
                          "description",
                      ],
                   }
                },
                "aliases": {
                   "type": "array",
                   "items": {
                      "type": "string"
                   }
                },
             },
             "required": [
                "name",
                "description",
             ]
          }
       },
       "required": [
           "data",
       ],
    }

    COMMAND_SCHEMA = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "uid": {
                        "type": "string"
                    },
                    "command": {
                        "type": "string"
                    },
                    "arguments": {
                        "type": "object"
                    },
                    "user_id": {
                        "type": "number"
                    },
                    "expires_at": {
                        "type": "number"
                    },
                    "messages_remaining": {
                        "type": "number"
                    },
                },
                "required": [
                    "uid",
                    "command",
                    "user_id"
                ]
            }
        },
        "required": [
            "data"
        ]
    }

    COMMANDRESPONSE_SCHEMA = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "uid": {
                        "type": "string"
                    },
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "uid",
                    "messages"
                ]
            }
        },
        "required": [
            "data"
        ]
    }

    ONLINELIST_SCHEMA = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "properties": {
                    "users": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": [
                    "users"
                ]
            }
        },
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
        elif actiontype == "registercommand":
            jsonschema.validate(instance=jsonData, schema=cls.REGISTERCOMMAND_SCHEMA)
        elif actiontype == "command":
            jsonschema.validate(instance=jsonData, schema=cls.COMMAND_SCHEMA)
        elif actiontype == "commandresponse":
            jsonschema.validate(instance=jsonData, schema=cls.COMMANDRESPONSE_SCHEMA)
        elif actiontype == "onlinelist":
            jsonschema.validate(instance=jsonData, schema=cls.ONLINELIST_SCHEMA)
        return True


if __name__ == "__main__":
    Validators.validateJson("onlinelist", {'command': 'onlinelist', 'data': {'users': ['SingingMango003', 'mchotwheels', 'contentw09', 'MyNinjaAlexYo', 'beansoup3rd', 'SteadyTripping', 'ShanksLinkerArm', 'SwiftTyrone', 'icetypelord123', 'skeetlmao', 'Ozzmosis', 'xcaiomaster', 'MrMixmess', 'nickwsgf', 'ALanEXita', 'GretelMk2', 'GymLeaderKyle', 'Silaris96', 'Vegeta079', 'Nuswin', 'Girachen', 'beafleaf', 'sethyboi', 'Ezwins', 'TheBearKoopa', 'aryanj7621', 'Grimes', 'hang105', 'theweekdy', 'TaintedProfessor', 'DooYEAH', 'BenXer', 'icecrem', 'pattisketcap1', 'Veigarbage', 'PBJelly', 'sarre', 'alvin770', 'Shadowpriest96', 'cjmbruh', 'Magal21', 'Gilthanas', 'Benmin', 'Tsuwuki', 'Tadaka', 'Yangsau5454', 'GrassMen', 'RRobzy', 'Ferax', 'tribra10', 'dmscullman', 'Error4O5', 'johnnysilver', 'CryoStorm', 'Raizeeel007', 'Xac', 'sup222', 'Caprical', 'Leau', 'Xzums', 'Sakrom9', 'KriticalHaze420', 'liroy', 'Levates', 'juliaaalala', 'SarosIV', 'LGBTQ69', 'Nirts', 'Menfis', 'Royse', 'DarkLatios1518', 'Brockeyes01', 'IBADDAY', 'Remington235845', 'Kingsoul77', 'Clevy', 'Zelenej01', 'Ralph99', 'HeavensLucifer', 'Medici', 'mrmctroll', 'Foxre', 'cryptidcat', 'davidbmaster', 'PauloBasado', 'Bahd', 'shellina', 'GanaManaRegen', 'Shinako', 'KuroShiroBW', 'ismachori18', 'Ysl', 'aimilianos', 'Nacho645', 'marianoo7', 'Animalreaper', 'Gurkensohn', 'hoodinit', 'IcePepsi', 'redfirejpg', 'Auburngreenwell', 'Leplusmeilleur', 'RayKroNos', 'MadSeason', 'IUchihaMIStall', 'RecycledPlastic', 'saulcano', 'lupelongo', 'Rambo824', 'NicklasOlsson', 'PalePhantom48', 'KAJOK3', 'cows123p', 'YourHotPsychiatrist', 'GLG', 'NagatinMAF', 'magnuskrogh', 'Whale109', 'Ivovic', 'Trevorsmash', 'boyee', 'watashixd', 'Skippi98', 'Killer1303', 'xMakeouthill', 'E3MXT7', 'Luker6', 'toefungus28', 'BigTitch420', 'jamaurirudley07', 'axilleas77', 'MrSurge', 'LilGoaty', 'yuhdeath', 'Carrazedas', 'mavaha', 'Carlosmoises', 'DanielSociety', 'Nakirium', 'CollectorTR', 'PapaAggron', 'smikkeldief123', 'bochu', 'TimmysWunderkiste', 'salamanz', 'Genbuguy2109', 'Doritoskitkat', 'NightRavenZ', 'KawakiChan', 'Maldorf', 'Milokit', 'Chaosreaper13', 'Galvantulaboi2015', 'ElderGimpy', 'Dreni', 'Artemiis', 'Sossle938', 'SHADOWJRK', 'iisn0ah', 'Flea22', 'cheeseyburger', 'AndreTheGiant57', 'KlimtG', 'jagged', 'cstdarkee', 'Ricardoo1110', 'Technox9', 'OutstandingRedneck225', 'MortisGame', 'DilanosKitten', 'lolofisk', 'mequana', 'CyborgPsycho', 'GodTakingADump', 'Logger1864', 'mgs07', 'MrPotaterman', 'Draxx777', 'Vide', 'Simyosh', 'flammkuchen07', 'defaultuser', 'ToonLinkGaming', 'Arto', 'Psam', 'KizeBooker', 'devenver', 'aves89', 'boytheblonde', 'Supermrjay', 'ynnc', 'MazenChad', 'farmakopoios', 'MrSaltbucket', 'Deniaxx3', 'TodaysTomorrow', 'tc056', 'PleasureBringer', 'knocksteady', 'uvxclassiikz', 'Azee', 'janedoe68111', 'Whoopsadaisy', 'Squog', 'AcidReign', 'Pacemakers', 'Cuatros', 'Portgas', 'DanceWithMeMax', 'Galante', 'cringecrab1123', 'kaua133', 'monatopotato', 'shwheelz', 'ghost23', 'Aidou', 'Junior790', 'TojiZenin', 'xnderAGB', 'alfredomorales19', 'Mazerus', 'ZaccPerKave', 'Darkangel008', 'Focus555', 'Red2223', 'Junker109', 'xavierthemaster', 'GenkiBaby', 'PowerfulSlash', 'Mnmboi1', 'nonvolatile', 'BloodCrowe', 'AldairCAGP', 'Morpers', 'akumarino', 'PolskiKrasnal', 'Rebel7', 'sumimasen', 'sylvur', 'Scuba6615', 'fudgefactory', 'Iydis', 'Henndor', 'Neo001992', 'eltecla', 'RxinFrxg', 'jeffvg98', 'BrookSibley', 'Frygid', 'SerPIMPalott', 'FrattyLight', 'Nicho', 'Syeq', 'DennyG', 'swalter333', 's20131020', 'MistyOaks', 'JayAdderz', 'Raptix', 'CaptainSnickersneeFan', 'BrucceLee', 'RoyalFire', 'Auntern', 'houseemily', 'Kingsbread', 'leviathan201285', 'Lelekoko', 'allmightysusan', 'Kyubey722', 'Fourkas', 'nekooncrack', 'JigglypuffsKnight', 'DuckIsMyName', 'coryespo', 'pangozillacard', 'Rzyn5462', 'LockeDy', 'Dagnabitt', 'somunaqe', 'SixtyNinex', 'lexxicon2', 'Vengeance07', 'Grahill', 'i4gothow2gro', 'cubbymw', 'FluXy', 'MongeShaolin', 'ADeJePecat', 'wsoryu2', 'PrevoAstro', 'darkwolf1209', 'Degere', 'Zimavyuga', 'qFx', 'Firmus', 'Lowkeyslayin', 'Darkness75', 'Anselmongoose', 'Alpi50', 'Lulusifer', 'Ayetrix', 'Tazwolf', 'cheerfulhelmet', 'TRIWIZARD', 'P1glet', 'kidmarvel4', 'LucVD47', 'resistance', 'Kebbs123', 'Nuncaachoshiny', 'faithums', 'Jaano', 'SpiekenJegen', 'MonstRsc2', 'dvqa123123', 'TaintedStone', 'BreakingTheQuiet', 'Leprechaunking', 'NeptuneGaming', 'Deareys', 'valhallabiorg', 'jhyegvrihydfthviygd1', 'OpoNoNo', 'Madziulka', 'Slickrick', 'pantheraG', 'diehllane', 'OtterSpace', 'msjeam', 'MassiWildt', 'PrimoPg', 'ImLowKeyLoki', 'UnDefeatedProGamer', 'unitytest69420', 'JStriker', 'gftrfyghvrf', 'KaioFTW', 'cowkicker73', 'fornix', 'JussThund3rr', 'StepanGhastly', 'DEUSgod', 'Caillougotcancer', 'Sanctus', 'misiub107', 'RedPandaBear', 'HenzzTrxsh7', 'TolgaLXZ', 'brandon8000', 'panz701', 'rencys', 'zllp', 'koeksje', 'TheShadowIX', 'ylan2002', 'bfo', 'ilmp825', 'ichicken21', 'Captain2', 'Feint', 'Wandinha', 'PattolinoXD', 'zorgax', 'EternatusEternamax', 'Mvnches', 'xCandyyy', 'AsuhTenan', 'cauafxp', 'danieltheworm', 'pedroz011', 'BabyBany11', 'G310', 'amazingorangatang23', 'DUMPIT', 'fast2furious', 'NME99', 'Jak1e', 'yangler', 'ProfWinship', 'PokeMitch', 'Mythsy', 'Raider18Moss', 'WhyMe7', 'KinSharkPKMN', 'chrollo590', 'Mpely', 'Acil112', 'GabsBank', 'SimisageMain', 'LolCoolName', 'goldenrod21', 'MKpokemon', 'misspiggy', 'Gust340', 'bozkurt2020', 'MGcorp55', 'caualegal123', 'Kejorn', 'Parkero983', 'ratsker', 'papabear75', 'Patrick100', 'Tahoomon', 'BillionDollarBaby', 'Zirtor', 'lexje100', 'Muerta', 'TheUndisputed88', 'xt2shirox', 'NeonGenius2023', 'tahashahkhan321', 'PeeWeeDee', 'milmil', 'DT456', 'MadameTerra', 'Lath', 'rocktrainershaun', 'kdogns1', 'bee2dota', 'Tarma', 'TonyBananza', 'Yanlee2023', 'llouwap', 'ObiCAM', 'leakyleak96', 'Mayadopapai', 'GeorgeK9', 'EConklinJR', 'theqerty', 'dryker', 'Sleetyy', 'Insignificance', 'DilanoSN', 'GiornoGoldenWind', 'miltos666', 'FurkanCTR', 'riicmoutinho', 'WaduhBro', 'XIIDEMONXII', 'Zelliox', 'NDGInferno', 'AZARADODEMAIS', 'PluggedOnYou', 'TheTopHatDragon', 'vaggiss', 'GraziMergina', 'Sholmes4491', 'TheKingSaucy', 'EriCocher', 'Excel2019', 'Gearzzz', 'ApothiconServant', 'pokemonrh', 'neoSama', 'Landirin', 'Toltor', 'FerrariRacer88', 'Validay', 'SecretAlt', 'PulsefireJer', 'BT7274', 'mrmimeisashsdad', 'ngoctai13x', 'Gabrielhdez10', 'ThePersonNextToYou', 'Sygll', 'Jieffecaliss', 'chaosporcupine', 'douglas878', 'Ankyra', 'sycosisme', 'ProfessorDolph', 'Kandata', 'suigetsu', 'Staraptor57', 'Kulrath', 'ukes', 'yeb0', 'SHALN4RK', 'KijnKer', 'SebusWingChun', 'Mpalancar', 'fitzy95', 'PetisoMatadorDePorco', 'Krelger', 'Cubby1988', 'cheeseb4ll', 'monipooh', 'cl8w', 'Dirkbeast', 'happynoobjordan2', 'DbOwen75', 'gabrielic', 'artyom29', 'StuffedCrustPizza', 'Matsuyaka', 'pedroo0066', 'venushero', 'KuraiLovesYou', 'LastSamurai', 'Leomia', 'dittokarma', 'Dearey', 'MapleMoon', 'Itsilow', 'undeadAC', 'QueenLilith', 'hyunpro123', 'pete379550', 'Loveen', 'shanebot1', 'Ameizing8', 'Asteria354', 'P1nglord', 'bbjmap', 'Runzerl', 'help0', 'Cor3x', 'arch4ang3lzz', 'SylveonFangirl', 'usuario666', 'kurukafant', 'janii', 'Pokevolo', 'issazak', 'coldwinter12', 'DrSmitty', 'abstar1236', 'MKhan', 'EduzinTK', 'SolarisShadowflame', 'bulletstorm94', 'teeking', 'noahninja100', 'bigboygames285', 'Jaxink', 'wajihtausif', 'bunny098765', 'RimuruStorm', 'Jeziah25', 'Stryker690', 'RoboxD', 'Copykitty2', 'suryk', 'Mantykee', 'OdeioSalada', 'Biqn', 'Praddle', 'SwordSaint12', 'Orianna20r', 'drxcarys', 'Vedelagop', 'LunaOfDeath', 'RobertJr', 'AttemptWithoutBots', 'Zelzarr', 'Rodristreet', 'GodAce12', 'PokeMasterLion', 'pinxy', 'XLCaaatttt', 'milkduddamar', 'Kohezja', 'Joyboy1905', 'Levayatan', 'IAteAToast76', 'PogTrainer', 'xrayspeckz', 'Salv1n0', 'capuchinho4', 'Romancefield', 'Melothy', 'lackeetrackee', 'Andyman99', 'mario445566', 'RugalKoff', 'Cadillako', 'DeYanne', 'Sliverkiller', 'Itzmouseyy', 'zhennie123', 'BLindCatcher', 'LangudN', 'AsmanJ', 'KingBulba', 'Come4me', 'ChickenNuggetKIng', 'batgirl1002', 'Sayua', 'jonascee', 'peterbookreader226', 'ZekSRB', 'Harley23', 'MissGeorgina', 'Kurveflet', 'kloro55', 'trailior', 'jessiep2201', 'peterlustig', 'THAC0', 'stormzy2x', 'opwinner12', 'ChickenLover1738', 'MasterKitten', 'Ace119', 'T3y', 'blandbat', 'BR33z3R', 'ZankaNoTachi', 'williammads', 'LRKing', 'Milthares', 'progamer6421', 'rollininmybenzo', 'TurnItUp', 'SzymonR', 'GiratinaDialga', 'Flameo456', 'MavensLost', 'RubyCurrant', 'kfc45', 'blackyurem99', 'ShadowZapdos954', 'hariskk', 'Toombz', 'mahoyoplayer', 'cassiuspeterson', 'sopgubben33', 'Instalock', 'BASIC98', 'DoiiDiinhO', 'UnicornOstard', 'LilyStriker', 'SavageBrewer999', 'DeVille', 'wutwutbunnyuni', 'AshijinCX', 'K2', 'Dxzwi', 'iamichu', 'Meryl', 'Ninja28483', 'Ash265', 'Derikk', 'osc54', 'GoldPenguin19', 'Proseufim', 'eastcoast50', 'ShkelzenLoveLixia', 'francowong4', 'partrbox', 'Shaytina', 'vectreira', 'ams', 'Thico', 'tristantodd', 'likwer', 'drtgvcfn2', 'charlesgabreilgonzaga', 'PeacemakerTimmy', 'ThatsTheMax', 'Jdkelley21', 'Fenylein', 'rodmarbrusas', 'MajesticTomato', 'Freevolo', 'dynmix', 'Lender22', 'Red', 'DasAuto', 'Hdillan', 'krakdotz', 'Remorse', 'TrainerDizzy', 'Oli23promax', 'Spirlashow', 'alwaysgoofy1', 'intelbrother', 'Dark360', 'Ximac', 'flpxzvd', 'CosmicEnergy', 'Flarebane', 'HoneyBadgee', 'crazymeco35', 'Macit', 'petrick20202', 'imfuccdup', 'nafx', 'comasz', 'Snoothy', 'Beastosoul', 'rotweissekatze', 'MissKiko', 'caspianBlackwood', 'Arazog', 'BVstarrr', 'Zyphril1010', 'PaulWalker', 'mrbeanxd', 'Plejdo', 'klfkenshin', 'Twoosty', 'jgarc221', 'MumbleWay', 'Glown', 'Demonology', 'philipnyberg1', 'MrKacer', 'sebasash', 'juninhu', 'ShadowTayab', 'bleidd93', 'PEPINILLO888', 'flemman123', 'Azevedo', 'MtScottC', 'Grifinix', 'VictorNikizinnn000', 'Illumiema24', 'matthewsoggy28', 'Lasagnita', 'crunchybigzilla1', 'inznayz', 'LampToast', 'MaryAlex', 'Powerslider87', 'Rivermore0', 'NeedForSwedeYT', 'kkwackegast', 'rother', 'LekkerSpelen', 'Kam1177', 'Jarstek', 'ThiCitruz', 'Ghezzal', 'mutabeareu', 'L0pez', 'khelerios', 'xLittleJohn', 'Salythecamelfish', 'SteveSkolo', 'UndamagedAxis', 'HyaProfOak', 'JB', 'Deadeye151', 'ellipsis97', 'Hebdieschere', 'dolcegusto95', 'nebgg', 'ASTROANGEL', 'Cooljimmy0120', 'tjkiller123', 'dxdvenom666', 'Umbop123', 'Abnerv', 'KolsiYassin', 'Monocaeros', 'AsianPokemontrainersIG', 'Yashdeep2001', 'eevilaOP', 'Belise208', 'hyperflux', 'p0gk0q', 'IronWolf416', 'Cuisinart', 'Taoko', 'Apple9', 'Reydragon', 'exuzin', 'Hyacks', 'Raxman14', 'ArielQuest', 'warsquirtle', 'O94scemitar', 'DallyyS', 'Kweam', 'DRick546', 'XxXPabloMarquesXxX', 'marioanddj', 'DestroLovesPokemon', 'ArturSilva', 'bluezokssa', 'Geminises', 'iAmHartnett', 'SvarTuR', 'Tscam', 'TomatoHead', 'Dansh', 'cheas', 'Shivboss777', 'steamedbunz', 'SKG57', 'FrozenKoala', 'Oblivous', 'mammon12', 'dragon6643', 'bolbol123', 'Nyktosia', 'dynamit', 'ToothlessLover', 'BigBoyDragonite', 'bonenmus', 'Abodov', 'Tses', 'Zarxes8', 'RoiMasutangu', 'kabibo', 'Ichbinnichtpeter', 'KingofReverseKin', 'TheGreatestSnowman', 'ShinyMegaGardevoir', 'sunnyd48', 'Aracnido', 'Charmanderboi', 'KynirSoDank', 'Infirmus', 'JustJustxn05', 'Maounis', 'Dormy6768', 'AjinnCX', 'thatguynotapi', 'Redikul', 'Cherrs', 'SinbadSama', 'Taka', 'ItsZay', 'Beckawaii', 'SolidWater1776', 'jax1003', 'urfavez', 'dharkon', 'JOEGRIGGS', 'hugecochrane', 'Aoqq', 'padespades', 'GHOSTDAWG', 'MyssMercy', 'SoloModz2', 'ShakeMyJake', 'Concora', 'sejereje', 'Jay8135', 'yeungsloth', 'zer0man', 'Alonsowcz', 'acsilver3', 'Altinordu', 'Danny95', 'ashsibling', 'Yuukimura', 'sniffytoes', 'Ingra', 'petroslol', 'LadyS', 'GodofDrakes', 'FaithWins', 'mickeyncurly', 'KingClash', 'Vocal', 'TheWolfslayer123', 'Ryke', 'Payt0n2304', 'Allan69', 'Splitgooch', 'flowageM', 'Muscletech', 'ThievingTub40', 'ashyratliff', 'vennizlouise', 'TheoDoore', 'helloimhere', 'pokekiller', 'oweny954', 'trw2001', 'l5555', 'Wayneman', 'fletchh43', 'Kyoma', 'LodMom', 'scoobylover123', 'ShadowDarkmidnait', 'RickDilson']}})