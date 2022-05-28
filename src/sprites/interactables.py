import pygame as pg
from src.utils import Spritesheet
from .sprite import Sprite
from .items import Item
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

        self.x = x
        self.y = y

        self.spritesheet = self.game.dcss1

        self.subtype = "chest"
        self.opened = False
        self.contents = None

    def open(self):
        if not self.opened:
            self.opened = True
            self.image = self.opened_img

            if self.contents:
                NotifyWin(self.game, 1,
                          f"Opened the {self.name.lower()}.",
                          f"Found {self.contents}").enter_state()
                Item(self.game, self.x, self.y, self.contents)
            else:
                NotifyWin(self.game, 1,
                          f"Opened the {self.name.lower()}.",
                          f"It's empty.").enter_state()


class WoodenChest(ChestCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.closed_img = self.spritesheet.image_at(44, 46, 1, 1)
        self.opened_img = self.spritesheet.image_at(45, 46, 1, 1)

        self.imgrect_center(self.closed_img)

        self.name = "Wooden Chest"

        self.contents = "Brass Key"
