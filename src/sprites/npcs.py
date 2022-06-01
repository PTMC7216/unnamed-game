import pygame as pg
from .sprite import Sprite
from src.allocs.stats import Stats
from src.states.dialoguewin import DialogueWin


class NPC:
    def __init__(self, game, x, y, npc_name):
        self.game = game

        npc_dict = {
            "Green Square": GreenSquare,
            "Yellow Square": YellowSquare,
            "Blue Square": BlueSquare
        }

        npc_dict[npc_name](game, x, y)


class NPCCon(Sprite, Stats):
    def __init__(self, game, x, y):
        self.game = game
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, game.npcs)

        Stats.__init__(
            self,
            lv=1,
            hp=9,
            mp=0,
            strength=1,
            dexterity=1,
            agility=1,
            vitality=1,
            intelligence=1,
            charisma=1,
            alignment=5)

        self.flags = []
        self.dialogue_section = "check"
        self.dialogue_counter = 0
        self.dialogue_memory = []

    def interact(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()

    def relocate(self, x, y):
        # TODO: create a Tiled object at the location an npc should relocate to, and send its position to this function
        self.rect.center = (x, y)


# Speaker type: only engages in dialogue
class GreenSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Green Square"


# Trader type: can open a trade window through dialogue
class YellowSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((150, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Yellow Square"


# Combatant type: only engages in combat
class BlueSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 0, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Blue Square"
