import pygame as pg
from .sprite import Sprite


class DoorCon(Sprite):
    def __init__(self, game, x, y, props):
        self.game = game
        self._layer = self.game.map_rect[3]
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, self.game.closed_doors)

        self.key_req = props["key_req"]
        if self.key_req is not None:
            self.desc = f"This door is locked with {self.key_req.split()[0].lower()}"

    def open(self):
        self.kill()
        self.add(self.game.opened_doors, self.game.all_sprites)
        self.image = self.opened_img


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


class Door:
    door_dict = {
        "Wooden Door": WoodenDoor,
        "Wooden Door Event": WoodenDoorEvent,
        "Wooden Gate NS": WoodenGateNS,
        "Wooden Gate WE": WoodenGateWE
    }

    def __init__(self, game, x, y, door_name, props):
        self.door_dict[door_name](game, x, y, props)
