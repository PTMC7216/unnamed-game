import pygame as pg
from src.utils import Spritesheet
from .sprite import Sprite
from .items import Item
from src.states.notifywin import NotifyWin, NotifyChoiceWin


class Interactable:
    def __init__(self, game, x, y, interactable_name):
        interactable_dict = {
            "Origin Space": OriginSpace,
            "Wooden Chest": WoodenChest
        }
        interactable_dict[interactable_name](game, x, y)


class SpaceCon(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = -2
        self.adjustable_layer = False
        Sprite.__init__(self, game, x, y, self.game.interactables)

        self.x = x
        self.y = y

        self.spritesheet = self.game.other_sheet

        self.subtype = "space"
        self.variance = 0
        self.step = 0


class OriginSpace(SpaceCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        img = self.spritesheet.image_at(7, 0, 1, 1)
        self.imgrect_center(img)

        self.name = "Origin Space"


class ChestCon(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = -2
        self.adjustable_layer = False
        Sprite.__init__(self, game, x, y, self.game.interactables)

        self.x = x
        self.y = y

        self.spritesheet = self.game.other_sheet

        self.subtype = "chest"
        self.opened = False
        self.contents = None

    def interact(self):
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

        self.closed_img = self.spritesheet.image_at(5, 0, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 0, 1, 1)

        self.imgrect_center(self.closed_img)

        self.name = "Wooden Chest"

        self.contents = None


class IronChest(ChestCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.closed_img = self.spritesheet.image_at(5, 1, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 1, 1, 1)

        self.imgrect_center(self.closed_img)

        self.name = "Iron Chest"

        self.contents = None
