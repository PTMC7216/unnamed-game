import math


class Stats:
    def __init__(self):

        self.lvl = 1

        self.strength = 1
        self.dexterity = 1
        self.agility = 1
        self.vitality = 1
        self.intelligence = 1
        self.charisma = 1

        # good: >10, neutral: 1-9, evil: <0
        self.alignment = 5

        self.hp = self.hp_mod(9)

        self.movespeed = 400

    def lvl_mod(self):
        pass

    def hp_mod(self, hp):
        return int(hp + math.pow(self.vitality, 1.4))
