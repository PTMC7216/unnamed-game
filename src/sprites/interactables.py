import pygame as pg
from src.utils import Spritesheet
from .sprite import Sprite
from src.states.notifywin import NotifyWin


class Interactable:
    def __init__(self, game, x, y, interactable_name):
        interactable_dict = {
            "Wooden Chest": WoodenChest
        }
        interactable_dict[interactable_name](game, x, y)


class ChestCon(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = -2
        self.adjustable_layer = False
        Sprite.__init__(self, game, x, y, self.game.interactables)

        self.spritesheet = self.game.dcss1

        self.subtype = "chest"

    def open(self):
        NotifyWin(self.game, 1,
                  f"Opened the {self.name.lower()}.",
                  f"It's empty.").enter_state()
        self.image = self.opened_img


class WoodenChest(ChestCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.closed_img = self.spritesheet.image_at(44, 46, 1, 1)
        self.opened_img = self.spritesheet.image_at(45, 46, 1, 1)

        self.imgrect_center(self.closed_img)

        self.name = "Wooden Chest"
