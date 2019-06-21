from django.db import models
from datetime import datetime


class Bracket:
    managed = False

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.roundOf16 = [
            {"name": "Pandemic"},
            {"name": "Captain Sonar"},
            {"name": "One Night Ultimate Werewolf"},
            {"name": "Code Names"},
            {"name": "Sherrif of Nottingham"},
            {"name": "Dead of Winter"},
            {"name": "Coup"},
            {"name": "7 Wonders"},
            {"name": "Ticket to Ride"},
            {"name": "Munchkin"},
            {"name": "Betrayal at House on the Hill"},
            {"name": "King of Tokyo"},
            {"name": "Photosynthesis"},
            {"name": "Settlers of Catan"},
            {"name": "Clank!"},
            {"name": "Dominion"},
        ]
        self.roundOf8 = [
            {"name": "Pandemic"},
            {"name": "Code Names"},
            {"name": "Dead of Winter"},
            {"name": "Coup"},
            {"name": "Munchkin"},
            {"name": "Betrayal at House on the Hill"},
            {"name": "Photosynthesis"},
            {"name": "Dominion"},
        ]
        self.semiFinals = [
            {"name": "Pandemic"},
            {"name": "Coup"},
            {"name": "Betrayal at House on the Hill"},
            {"name": "Dominion"},
        ]
        self.finals = [
            {"name": "Pandemic"},
            {"name": "Dominion"},
        ]
        self.winner = {"name": "Pandemic"}


class Tourney(models.Model):
    title = models.CharField(max_length=200)
    match_duration = models.IntegerField(default=15)
    start_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.id) + ": " + str(self.title)


class Character(models.Model):
    name = models.CharField(max_length=200)
    tourney = models.ForeignKey(Tourney, on_delete=models.CASCADE, related_name="characters")

    def __str__(self):
        return str(self.id) + ": " + str(self.name)


class Match(models.Model):
    tourney = models.ForeignKey(Tourney, on_delete=models.CASCADE, null=True)
    sequence = models.IntegerField(default=0)
    character1 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="character1", null=True)
    character2 = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="character2", null=True)
    winner = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)
    mom = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="child1")
    dad = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="child2")
    round = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + ": " + str(self.character1) + " vs " + str(self.character2)


class Vote(models.Model):
    username = models.CharField(max_length=200)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True, related_name="votes")
    character = models.ForeignKey(Character, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.username) + " votes for " \
               + str(self.character.name)
