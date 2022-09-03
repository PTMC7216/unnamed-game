import math


class Stats:
    def __init__(self, lv, hp, mp, strength, dexterity, agility, vitality, intelligence, charisma, alignment):

        # equipment
        self.hand = ['None'] * 2
        self.accessory = ['None'] * 2
        self.head = 'None'
        self.torso = 'None'
        self.hands = 'None'
        self.legs = 'None'
        self.feet = 'None'

        # stats
        self.lv = lv
        self.strength = strength
        self.dexterity = dexterity
        self.agility = agility
        self.vitality = vitality
        self.intelligence = intelligence
        self.charisma = charisma
        self.hp = self.hp_mod(hp)
        self.mp = mp
        self.unallocated = 0
        # good: >9, neutral: 1-9, evil: <1
        # TODO: confirmation via NotifyChoiceWin to attack non-hostiles if alignment > 0
        self.alignment = alignment
        self.movespeed = 300

        # substats
        self.attack_power = math.pow(self.strength, 1.4)

    def attack_power_update(self):
        power = 0
        for item in self.hand:
            if item != 'None':
                power += item.damage
        power += math.pow(self.strength, 1.4)
        self.attack_power = power

    def lvl_mod(self, lvl):
        pass

    def hp_mod(self, hp):
        return int(hp + math.pow(self.vitality, 1.4))

    def update_lvl(self):
        pass

    def attack(self, target):
        target.hp += -self.attack_power
        print(target.hp)

    def update_substats(self):
        self.attack_power_update()
