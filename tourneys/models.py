from django.db import models


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

    def __str__(self):
        return self.title


class Character(models.Model):
    name = models.CharField(max_length=200)
    tourney = models.ForeignKey(Tourney, on_delete=models.CASCADE, related_name="characters")

    def __str__(self):
        return self.name


class RoundContestant(models.Model):
    round = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    tourney = models.ForeignKey(Tourney, on_delete=models.CASCADE, related_name="round_contestants", null=True)

    def __str__(self):
        return str(self.id) + ": " + "round " + str(self.round) + " - " + str(self.character)


class Match(models.Model):
    contestant1 = models.ForeignKey(RoundContestant, on_delete=models.CASCADE, related_name="contestant1")
    contestant2 = models.ForeignKey(RoundContestant, on_delete=models.CASCADE, related_name="contestant2")

    def __str__(self):
        return str(self.id) + ": " + str(self.contestant1.character) + " vs " + str(self.contestant2.character)


class Vote(models.Model):
    username = models.CharField(max_length=200)
    round_contestant = models.ForeignKey(RoundContestant, on_delete=models.CASCADE, related_name="votes", null=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.round_contestant.round) + ": " + str(self.username) + " votes for " \
               + str(self.round_contestant.character)
