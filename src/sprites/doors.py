import pygame as pg
from .sprite import Sprite
from src.states.notifywin import NotifyWin


class DoorCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = game.map_rect[3], True
        super().__init__(game, x, y, game.closed_doors)
        self.category = "door"
        self.key_req = None

        if props:
            if "key_req" in props:
                self.key_req = props["key_req"]
                self.desc = f"This door is locked with {self.key_req.split()[0].lower()}"

            if "shield_type" in props:
                self.shield_type = props["shield_type"]
                self.desc = f"This door is shielded by a layer of {self.shield_type.lower()} energy"

    def open(self):
        self.kill()
        self.add(self.game.opened_doors, self.game.all_sprites)
        self.image = self.opened_img

    def interact(self):
        if self.key_req is None:
            self.open()
            NotifyWin(self.game, 1, f"Opened the {self.name.lower()}.").enter_state()
        else:
            NotifyWin(self.game, 1, f"{self.desc}.").enter_state()


class WoodenDoor(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.game.other_sheet.image_at(0, 0, 1, 1)
        self.opened_img = self.game.other_sheet.image_at(0, 1, 1, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = "Wooden Door"


class WoodenDoorEvent(WoodenDoor):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)

    def open(self):
        self.set_flag("Yellow Test", "door opened")
        self.kill()
        self.add(self.game.opened_doors, self.game.all_sprites)
        self.image = self.opened_img


class WoodenGateNS(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.game.other_sheet.image_at(1, 0, 2, 1)
        self.opened_img = self.game.other_sheet.image_at(1, 1, 2, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = "Wooden Gate"


class WoodenGateWE(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.game.other_sheet.image_at(3, 0, 1, 2)
        self.opened_img = self.game.other_sheet.image_at(4, 0, 1, 2)
        self.imgrect_topleft(self.closed_img)
        self.name = "Wooden Gate"


class EnergyDoor(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.shield_type == "green":
            self.closed_img = self.game.other_sheet.image_at(0, 3, 1, 1)
        self.opened_img = self.game.other_sheet.image_at(0, 1, 1, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = "Force Door"
        self.shielded = True

    def interact(self):
        if self.shielded:
            NotifyWin(self.game, 1, f"{self.desc}.").enter_state()


class Door:
    door_dict = {
        "Wooden Door": WoodenDoor,
        "Wooden Door Event": WoodenDoorEvent,
        "Wooden Gate NS": WoodenGateNS,
        "Wooden Gate WE": WoodenGateWE,
        "Energy Door": EnergyDoor,
    }

    def __init__(self, game, x, y, door_name, props):
        self.door_dict[door_name](game, x, y, props)
