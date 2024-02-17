from abc import ABC
from api.ingame_data.models.eventname import Eventname
from api.highscores.models.highscoreconfig import HighscoreConfig
from django.core.management.base import BaseCommand
from api.ingame_data.models import Encounter
import datetime
import random


class Command(BaseCommand, ABC):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **options):
        # self._seedEventNames()
        # self._seedHighscoreConfigs()
        self._seedEncounters()

    def _seedEventNames(self):
        Eventname.objects.bulk_create([
            Eventname(name="arceusaltar", fields={}),
            Eventname(name="chest", fields={}),
            Eventname(name="clanwars", fields={}),
            Eventname(name="dianciealtar", fields={}),
            Eventname(name="elite4", fields={}),
            Eventname(name="encounter", fields={}),
            Eventname(name="goldrush", fields={}),
            Eventname(name="honey", fields={}),
            Eventname(name="itembomb", fields={}),
            Eventname(name="kyogrealtar", fields={}),
            Eventname(name="roll", fields={}),
            Eventname(name="serverrestart", fields={}),
            Eventname(name="swarm", fields={}),
            Eventname(name="tournament", fields={}),
            Eventname(name="worldblessing", fields={}),
            Eventname(name="worldboss", fields={}),
        ])

    def _seedHighscoreConfigs(self):
        HighscoreConfig.objects.bulk_create([
            HighscoreConfig(highscorename="ancientcavemapcontrol", url="https://pokemon-planet.com/ancientCave.php", pagesamount=1, fieldmapping={"clan": "Clan Name", "pokemon_defeated": "Pokemon Defeated"}, verbose_name="Ancient Cave Map Control", intfields={"clan": 0, "pokemon_defeated": 1}),
            HighscoreConfig(highscorename="battlezonemapcontrol", url="https://pokemon-planet.com/battleZoneMapControl.php", pagesamount=1, fieldmapping={"clan": "Clan Name", "pokemon_defeated": "Pokemon Defeated"}, verbose_name="Battle Zone Map Control", intfields={"clan": 0, "pokemon_defeated": 1}),
            HighscoreConfig(highscorename="btwins", url="https://pokemon-planet.com/btWins.php", pagesamount=1, fieldmapping={"wins": "Wins", "username": "Username", "winstreak": "Win Streak"}, verbose_name="Most Battle Tower Wins", intfields={"wins": 1, "username": 0, "winstreak": 1}),
            HighscoreConfig(highscorename="btwinstreak", url="https://pokemon-planet.com/btWinStreak.php", pagesamount=1, fieldmapping={"wins": "Wins", "username": "Username", "winstreak": "Win Streak"}, verbose_name="Top Battle Tower Win Streak", intfields={"wins": 1, "username": 0, "winstreak": 1}),
            HighscoreConfig(highscorename="clanwarwins", url="https://pokemon-planet.com/clanWarWins.php", pagesamount=1, fieldmapping={"clan": "Clan", "wins": "Wins"}, verbose_name="Most Clan War Wins", intfields={"clan": 0, "wins": 1}),
            HighscoreConfig(highscorename="littlecupbattlewins", url="https://pokemon-planet.com/tournamentBattleWins5.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Most Little Cup Battle Wins", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="littlecupratings", url="https://pokemon-planet.com/tournamentRatings5.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Best Little Cup Ratings", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 1}),
            HighscoreConfig(highscorename="littlecupwins", url="https://pokemon-planet.com/tournamentWins5.php", pagesamount=1, fieldmapping={"wins": "Wins", "rating": "Rating", "username": "Username"}, verbose_name="Most Little Cup Tournament Wins", intfields={"wins": 1, "rating": 1, "username": 1}),
            HighscoreConfig(highscorename="monotypebattlewins", url="https://pokemon-planet.com/tournamentBattleWins4.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Most Monotype Battle Wins", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="monotyperatings", url="https://pokemon-planet.com/tournamentRatings4.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Best Monotype Ratings", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="monotypewins", url="https://pokemon-planet.com/tournamentWins4.php", pagesamount=1, fieldmapping={"wins": "Wins", "rating": "Rating", "username": "Username"}, verbose_name="Most Monotype Tournament Wins", intfields={"wins": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="mostpokemonboxes", url="https://pokemon-planet.com/mostPokemonBoxes.php", pagesamount=10, fieldmapping={"clan": "Clan", "opened": "Pokemon Boxes Opened", "username": "Username"}, verbose_name="Most Pokemon Boxes Opened", intfields={"clan": 0, "opened": 1, "username": 0}),
            HighscoreConfig(highscorename="playerclanwarwins", url="https://pokemon-planet.com/playerClanWarWins.php", pagesamount=10, fieldmapping={"clan": "Clan", "wins": "Wins", "losses": "Losses", "username": "Username", "wins_losses": "Wins-Losses"}, verbose_name="Most Clan War Battle Wins", intfields={"clan": 0, "wins": 1, "losses": 1, "username": 0, "wins_losses": 1}),
            HighscoreConfig(highscorename="playerclanwarwinslosses", url="https://pokemon-planet.com/playerClanWarWinsLosses.php", pagesamount=10, fieldmapping={"clan": "Clan", "wins": "Wins", "losses": "Losses", "username": "Username", "wins_losses": "Wins-Losses"}, verbose_name="Top Performing Trainers (Clan Wars)", intfields={"clan": 0, "wins": 1, "losses": 1, "username": 0, "wins_losses": 1}),
            HighscoreConfig(highscorename="safarizonemapcontrol", url="https://pokemon-planet.com/safariZoneMapControl.php", pagesamount=1, fieldmapping={"clan": "Clan Name", "pokemon_defeated": "Pokemon Defeated"}, verbose_name="Safari Zone Map Control", intfields={"clan": 0, "pokemon_defeated": 1}),
            HighscoreConfig(highscorename="selfcaughtbattlewins", url="https://pokemon-planet.com/tournamentBattleWins1.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Most Self Caught Battle Wins", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="selfcaughtratings", url="https://pokemon-planet.com/tournamentRatings1.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Best Self Caught Ratings", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="selfcaughtwins", url="https://pokemon-planet.com/tournamentWins1.php", pagesamount=1, fieldmapping={"wins": "Wins", "rating": "Rating", "username": "Username"}, verbose_name="Most Self Caught Tournament Wins", intfields={"wins": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="setlevelbattlewins", url="https://pokemon-planet.com/tournamentBattleWins2.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Most Set Level Battle Wins", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="setlevelratings", url="https://pokemon-planet.com/tournamentRatings2.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Best Set Level Ratings", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="setlevelwins", url="https://pokemon-planet.com/tournamentWins2.php", pagesamount=1, fieldmapping={"wins": "Wins", "rating": "Rating", "username": "Username"}, verbose_name="Most Set Level Tournament Wins", intfields={"wins": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="topachievements", url="https://pokemon-planet.com/mostAchievements.php", pagesamount=10, fieldmapping={"clan": "Clan", "username": "Username", "achievements": "Achievements Completed"}, verbose_name="Top Achievements", intfields={"clan": 0, "username": 0, "achievements": 1}),
            HighscoreConfig(highscorename="topdex", url="https://pokemon-planet.com/mostPokemonOwned.php", pagesamount=10, fieldmapping={"clan": "Clan", "pokemon": "Unique Pokemon Caught/Evolved", "username": "Username"}, verbose_name="Most Unique Pokemon Caught", intfields={"clan": 0, "pokemon": 1, "username": 0}),
            HighscoreConfig(highscorename="topevoboxes", url="https://pokemon-planet.com/mostEvoBoxes.php", pagesamount=10, fieldmapping={"clan": "Clan", "opened": "Evo Boxes Opened", "username": "Username"}, verbose_name="Most Evolutional Stone Boxes Opened", intfields={"clan": 0, "opened": 1, "username": 0}),
            HighscoreConfig(highscorename="topfishing", url="https://pokemon-planet.com/topFishers.php", pagesamount=10, fieldmapping={"clan": "Clan", "level": "Fishing Level", "username": "Username", "experience": "Fishing Experience"}, verbose_name="Top Fishers", intfields={"clan": 0, "level": 1, "username": 0, "experience": 1}),
            HighscoreConfig(highscorename="toplle", url="https://pokemon-planet.com/topLLE.php", pagesamount=10, fieldmapping={"lle": "LLE", "clan": "Clan", "username": "Username"}, verbose_name="Top LLE", intfields={"lle": 1, "clan": 1, "username": 1}),
            HighscoreConfig(highscorename="topmining", url="https://pokemon-planet.com/topMiners.php", pagesamount=10, fieldmapping={"clan": "Clan", "level": "Mining Level", "username": "Username", "experience": "Mining Experience"}, verbose_name="Top Miners", intfields={"clan": 0, "level": 1, "username": 0, "experience": 1}),
            HighscoreConfig(highscorename="topmysteryboxes", url="https://pokemon-planet.com/mostMysteryBoxes.php", pagesamount=10, fieldmapping={"clan": "Clan", "opened": "Mystery Boxes Opened", "username": "Username"}, verbose_name="Most Mystery Boxes Opened", intfields={"clan": 0, "opened": 1, "username": 0}),
            HighscoreConfig(highscorename="topphilanthropists", url="https://pokemon-planet.com/topPhilanthropists.php", pagesamount=10, fieldmapping={"pp": "Philanthropist Points", "clan": "Clan", "username": "Username"}, verbose_name="Top Philanthropists", intfields={"pp": 1, "clan": 0, "username": 0}),
            HighscoreConfig(highscorename="toprichest", url="https://pokemon-planet.com/topRichest.php", pagesamount=10, fieldmapping={"clan": "Clan", "money": "Money", "username": "Username"}, verbose_name="Top Richest", intfields={"clan": 0, "money": 1, "username": 0}),
            HighscoreConfig(highscorename="toprichestclans", url="https://pokemon-planet.com/topRichestClans.php", pagesamount=1, fieldmapping={"bank": "Clan Bank", "clan": "Name", "founder": "Founder"}, verbose_name="Top Richest Clans", intfields={"bank": 1, "clan": 0, "founder": 0}),
            HighscoreConfig(highscorename="topstrongest", url="https://pokemon-planet.com/topStrongest.php", pagesamount=10, fieldmapping={"clan": "Clan", "username": "Username", "experience": "Cumulative Experience"}, verbose_name="Top Strongest", intfields={"clan": 0, "username": 0, "experience": 1}),
            HighscoreConfig(highscorename="topstrongestclans", url="https://pokemon-planet.com/topStrongestClans.php", pagesamount=1, fieldmapping={"clan": "Name", "founder": "Founder", "experience": "Clan Experience"}, verbose_name="Top Strongest Clans", intfields={"clan": 0, "founder": 0, "experience": 1}),
            HighscoreConfig(highscorename="topworldbossdamage", url="https://pokemon-planet.com/mostWorldBossDamage.php", pagesamount=10, fieldmapping={"clan": "Clan", "username": "Username", "total_damage": "Total Damage"}, verbose_name="Most World Boss Damage", intfields={"clan": 0, "username": 0, "total_damage": 1}),
            HighscoreConfig(highscorename="ubersbattlewins", url="https://pokemon-planet.com/tournamentBattleWins3.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Most Ubers Battle Wins", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="ubersratings", url="https://pokemon-planet.com/tournamentRatings3.php", pagesamount=1, fieldmapping={"wins": "Wins", "losses": "Losses", "rating": "Rating", "username": "Username"}, verbose_name="Best Ubers Ratings", intfields={"wins": 1, "losses": 1, "rating": 1, "username": 0}),
            HighscoreConfig(highscorename="uberswins", url="https://pokemon-planet.com/tournamentWins3.php", pagesamount=1, fieldmapping={"wins": "Wins", "rating": "Rating", "username": "Username"}, verbose_name="Most Ubers Tournament Wins", intfields={"wins": 1, "rating": 1, "username": 0}),

        ])

    def _seedEncounters(self):
        self.stdout.write(self.style.SUCCESS('Seeding encounters'))

        # Adding encounters to a list cause bulk-creating is faster.
        encounters = []
        for i in range(1, random.randint(10000, 10000)):
            encounters.append(
                Encounter(
                    player=f"player{random.randint(1, 100)}",
                    pokemon=f"pokemon{random.randint(1, 100)}",
                    date=datetime.date.today() - datetime.timedelta(days=random.randint(1, 365)),
                    level=random.randint(1, 120)
                )
            )

        Encounter.objects.bulk_create(encounters)

        self.stdout.write(self.style.SUCCESS('Seeded encounters'))
