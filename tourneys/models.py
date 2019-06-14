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
