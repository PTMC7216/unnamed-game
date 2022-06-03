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

        self.relocation = 0

    def interact(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()

    def relocate(self):
        for relocator in self.game.relocators:
            if self.name in relocator.name:
                if self.relocation == relocator.relocation:
                    self.rect = Rect(relocator.x, relocator.y, relocator.w, relocator.h)
                    break


class Cleaner(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__(self.game.cleaner)

        self.rect = pg.Rect(x, y, w, h)
        self.x, self.y = x, y


class Relocator:
    def __init__(self, game, x, y, w, h, name):
        self.game = game
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.name = name

        nums = []
        contained = False
        for char in self.name:
            if char == "(":
                contained = True
            elif contained and char.isdigit():
                nums.append(char)
            elif char == ")":
                contained = False
        self.relocation = "".join(nums)

        self.game.relocators.append(self)


class Obstacles(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        super().__init__(self.game.obstacles)

        self.rect = pg.Rect(x, y, w, h)
