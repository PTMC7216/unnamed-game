import pygame as pg
from src.states.dialoguewin import DialogueWin


class Entity(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__(self.game.entity)

        self.rect = pg.Rect(x, y, w, h)

        self.name = "? ? ?"

        self.flags = []
        self.dialogue_section = "check"
        self.dialogue_counter = 0
        self.dialogue_memory = []

    def interact(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()

    def relocate(self):
        # TODO: finish relocate func in NPCCon, then copy it here
        pass


class Cleaner(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__(self.game.cleaner)

        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y


class Obstacles(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__(self.game.obstacles)

        self.rect = pg.Rect(x, y, w, h)
