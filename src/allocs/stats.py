import math


class Stats:
    def __init__(self, lvl, hp, strength, dexterity, agility, vitality, intelligence, charisma, alignment):

        self.lvl = lvl

        self.strength = strength
        self.dexterity = dexterity
        self.agility = agility
        self.vitality = vitality
        self.intelligence = intelligence
        self.charisma = charisma

        self.hp = self.hp_mod(hp)

        # good: >9, neutral: 1-9, evil: <1
        # TODO: confirmation to attack non-hostiles if alignment > 0
        self.alignment = alignment

        self.movespeed = 400

        self.hand = [""] * 2
        self.accessory = [""] * 4
        self.head = ""
        self.torso = ""
        self.gloves = ""
        self.legs = ""
        self.boots = ""

    def lvl_mod(self, lvl):
        pass

    def hp_mod(self, hp):
        return int(hp + math.pow(self.vitality, 1.4))

    def update_lvl(self):
        pass

    def attack(self, target):
        target.hp += -self.strength
        print(target.hp)
