import sqlite3
from abc import ABC

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from api.eventconfigurations.models import Eventconfiguration, Playerconfig, EventconfigPermissions, Clanconfig
from api.highscores.models import DefaultClanname
from api.ingame_data.models import *
import datetime


class Command(BaseCommand, ABC):
    help = 'migrates data from the sqlite databases'
    ingamedatadb = "ingame_data.db"
    configurationsdatabase = "eventconfigurations.db"
    highscoresdatabase = "highscores.db"

    def handle(self, *args, **options):
        self.__migrateDefaultClanname()
        self.__migrateChests()
        self.__migrateEncounters()
        self.__migrateRolls()
        self.__migrateEventConfigs()
        self.__migrateActivity()
        self.__migrateClanconfig()
        self.__migratePlayerconfig()
        self.__migrateEventconfigPermissions()

    def __migrateDefaultClanname(self):
        with sqlite3.connect(self.highscoresdatabase) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clannames")

            defaultclannames = []
            for row in cur.fetchall():
                if row[1] is None:
                    continue
                defaultclannames.append(DefaultClanname(guild=row[0], clan=row[1]))
            DefaultClanname.objects.bulk_create(defaultclannames)

    def __migrateChests(self):
        with sqlite3.connect(self.ingamedatadb) as conn:
            cur = conn.cursor()
            cur.execute("SELECT location, player, date from chests")
            chests = []

            for row in cur.fetchall():
                chests.append(Chest(location=row[0], player=row[1],
                                    date=datetime.datetime.strptime(row[2], '%Y-%m-%d').date()))
            Chest.objects.bulk_create(chests)

    def __migrateEncounters(self):
        with sqlite3.connect(self.ingamedatadb) as conn:
            cur = conn.cursor()
            cur.execute("SELECT Encounters, Name, Date FROM encounters")
            encounters = []

            for row in cur.fetchall():
                encounters.append(Encounter(pokemon=row[0], player=row[1],
                                    date=datetime.datetime.strptime(row[2], '%Y-%m-%d').date()))

            Encounter.objects.bulk_create(encounters)

    def __migrateRolls(self):
        with sqlite3.connect(self.ingamedatadb) as conn:
            cur = conn.cursor()
            cur.execute("SELECT pokemon, player, date FROM rolls")
            rolls = []

            for row in cur.fetchall():
                rolls.append(Roll(pokemon=row[0], player=row[1],
                                    date=datetime.datetime.strptime(row[2], '%Y-%m-%d').date()))
            Roll.objects.bulk_create(rolls)

    def __migrateEventConfigs(self):
        with sqlite3.connect(self.configurationsdatabase) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM eventconfig")

            eventconfigs = []
            for row in cur.fetchall():
                eventname, created = Eventname.objects.get_or_create(name=row[1])
                if created:
                    eventname.save()

                eventconfigs.append(Eventconfiguration(guild=row[0], eventname=eventname, channel=row[2], pingrole=row[3],
                                   time_in_channel=row[4]))
            Eventconfiguration.objects.bulk_create(eventconfigs)

    def __migrateActivity(self):
        with sqlite3.connect(self.ingamedatadb) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM activity")
            activities = []
            for row in cur.fetchall():
                activities.append(Activity(player=row[0],
                                           lastonline=datetime.datetime.fromtimestamp(int(row[1]), datetime.timezone.utc)))
            Activity.objects.bulk_create(activities)

    def __migrateClanconfig(self):
        with sqlite3.connect(self.configurationsdatabase) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM clanconfig")

            clanconfigs = []
            for row in cur.fetchall():
                clanconfigs.append(Clanconfig(guild=row[0], clan=row[1]))

            Clanconfig.objects.bulk_create(clanconfigs)

    def __migratePlayerconfig(self):
        with sqlite3.connect(self.configurationsdatabase) as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM memberconfig")

            for row in cur.fetchall():

                pconfig = Playerconfig(guild=row[0], player=row[1])
                try:
                    pconfig.save()
                except IntegrityError as e:
                    print(e, row)

    def __migrateEventconfigPermissions(self):
        with sqlite3.connect(self.configurationsdatabase) as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM permissions")

            permissions = []
            for row in cur.fetchall():
                permissions.append(EventconfigPermissions(guild=row[0], role=row[1]))
            EventconfigPermissions.objects.bulk_create(permissions)
