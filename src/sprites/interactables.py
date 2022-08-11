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
        self.event = False
        self.flagged_npc = None
        self.flagged_desc = None

        if props:
            if "crystal_type" in props:
                self.crystal_type = props["crystal_type"]

            if "event" in props:
                self.event = True
                self.flagged_npc = props["flagged_npc"]
                self.flagged_desc = props["flagged_desc"]

    def interact(self):
        NotifyWin(self.game, 1, f"{self.desc}.").enter_state()


class CrystalSwitch(SwitchCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.crystal_type == "green":
            self.active_img = self.spritesheet.image_at(6, 3, 1, 1)
        elif self.crystal_type == "red":
            self.active_img = self.spritesheet.image_at(7, 3, 1, 1)
        self.inert_img = self.spritesheet.image_at(5, 3, 1, 1)
        self.imgrect_topleft(self.active_img)
        self.name = "Crystal Switch"
        self.active = True

    def interact(self):
        if self.active:
            NotifyChoiceWin(self.game, self.name,
                            "Do nothing", "Touch it", 0, 1,
                            f"{self.crystal_type.capitalize()} energy swirls within this crystal").enter_state()
        else:
            NotifyWin(self.game, 1, "The crystal is powerless.").enter_state()


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
        self.imgrect_topleft(img)
        self.name = "Origin Space"

    def interact(self):
        # TODO: Origin Space interaction
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
            if "contents" in props:
                self.contents = props["contents"]

            if "key_req" in props:
                self.key_req = props["key_req"]
                self.desc = f"It's locked with {self.key_req.split()[0].lower()}"

            if "opened" in props:
                self.opened = props["opened"]

    def open(self):
        self.opened = True
        self.image = self.opened_img

    def interact(self):
        notices = []
        switch = False

        if not self.opened:
            if self.key_req is None:
                self.open()
                switch = True
                notices.append(f"Opened the {self.name.lower()}.")
            else:
                NotifyWin(self.game, 1, f"{self.desc}.").enter_state()

        if self.opened:
            if not switch:
                notices.append(f"Looked inside the {self.name.lower()}.")
            if self.contents:
                notices.append(f"Found {self.contents}.")
                NotifyWin(self.game, 1, *notices).enter_state()
                Item(self.game, self.x, self.y, self.contents)
                self.contents = None
            else:
                notices.append("It's empty.")
                NotifyWin(self.game, 1, *notices).enter_state()


class WoodenChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 0, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 0, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = "Wooden Chest"


class IronChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 1, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 1, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = "Iron Chest"


class CoffinChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 2, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 2, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = "Coffin"


class Interactable:
    interactable_dict = {
        "Crystal Switch": CrystalSwitch,
        "Map Portal": MapPortal,
        "Origin Space": OriginSpace,
        "Wooden Chest": WoodenChest,
        "Iron Chest": IronChest,
        "Coffin Chest": CoffinChest
    }

    def __init__(self, game, x, y, interactable_name, props):
        self.interactable_dict[interactable_name](game, x, y, props)
