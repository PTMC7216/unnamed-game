import pygame as pg
from src.states.dialoguewin import DialogueWin
from src.utils import Spritesheet
from .stats import Stats


class NPC:
    def __init__(self, game, x, y, npc_name):
        self.game = game

        npc_dict = {
            "Green Square": GreenSquare,
            "Blue Square": BlueSquare
        }

        npc_dict[npc_name](game, x, y)


class NPCCon(pg.sprite.Sprite, Stats):
    def __init__(self, game):
        self.game = game
        self.adjustable_layer = True
        pg.sprite.Sprite.__init__(self, self.game.npcs, self.game.all_sprites)

        Stats.__init__(self)
        self.hostility = 0

        self.dialogue_section = "check"
        self.dialogue_counter = 0
        self.dialogue_memory = []

    def interaction(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()


class GreenSquare(NPCCon):
    def __init__(self, game, x, y):
        NPCCon.__init__(self, game)

        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # self.spritesheet = Spritesheet(self.game, 'name.png')
        # self.image = self.spritesheet.image_at(1, 0, 1, 1)
        # self.rect = self.image.get_rect()
        # self.rect.center = (x, y)

        self.name = "Green Square"


class BlueSquare(NPCCon):
    def __init__(self, game, x, y):
        NPCCon.__init__(self, game)

        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 0, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Blue Square"
