import pygame as pg
from src.utils import Spritesheet
from .sprite import Sprite
from .items import Item
from src.states.notifywin import NotifyWin, NotifyChoiceWin


class SwitchCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = -2, False
        super().__init__(game, x, y, game.interactables)
        self.spritesheet = game.other_sheet
        self.category = "switch"


class GreenCrystalSwitch(SwitchCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.active_img = self.spritesheet.image_at(6, 2, 1, 1)
        self.inert_img = self.spritesheet.image_at(5, 2, 1, 1)
        self.imgrect_center(self.active_img)
        self.name = "Green Crystal"


class PortalCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = -2, False
        super().__init__(game, x, y, spritegroup)
        self.spritesheet = game.other_sheet
        self.category = "portal"


class MapPortal(PortalCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)


class SpaceCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = -2, False
        super().__init__(game, x, y, game.interactables)
        self.spritesheet = game.other_sheet
        self.category = "space"
        self.variance = 0
        self.step = 0


class OriginSpace(SpaceCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        img = self.spritesheet.image_at(7, 0, 1, 1)
        self.imgrect_center(img)
        self.name = "Origin Space"

    def interact(self):
        pass


class ChestCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = -2, False
        super().__init__(game, x, y, game.interactables)
        self.spritesheet = game.other_sheet
        self.category = "chest"
        self.opened = False
        self.key_req = None
        self.contents = None

        if props:
            if props["key_req"]:
                self.key_req = props["key_req"]
                self.desc = f"This chest is locked with {self.key_req.split()[0].lower()}"

    def open(self):
        self.opened = True
        self.image = self.opened_img

    def interact(self):
        if not self.opened:
            if self.key_req is None:
                self.open()
                if self.contents:
                    NotifyWin(self.game, 1,
                              f"Opened the {self.name.lower()}.",
                              f"Found {self.contents}").enter_state()
                    Item(self.game, self.x, self.y, self.contents)
                else:
                    NotifyWin(self.game, 1,
                              f"Opened the {self.name.lower()}.",
                              f"It's empty.").enter_state()
            else:
                NotifyWin(self.game, 1, f"{self.desc}.").enter_state()


class WoodenChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 0, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 0, 1, 1)
        self.imgrect_center(self.closed_img)
        self.name = "Wooden Chest"
        self.contents = None


class IronChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 1, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 1, 1, 1)
        self.imgrect_center(self.closed_img)
        self.name = "Iron Chest"
        self.contents = None


class Interactable:
    interactable_dict = {
        "Map Portal": MapPortal,
        "Origin Space": OriginSpace,
        "Wooden Chest": WoodenChest,
        "Iron Chest": IronChest
    }

    def __init__(self, game, x, y, interactable_name, props):
        self.interactable_dict[interactable_name](game, x, y, props)
