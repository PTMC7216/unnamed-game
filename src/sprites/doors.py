import pygame as pg
from .sprite import Sprite


class Door:
    def __init__(self, game, x, y, door_name):
        door_dict = {
            "Wooden Door": WoodenDoor,
            "Wooden Double Door NS": WoodenDoubleDoorNS,
            "Wooden Double Door WE": WoodenDoubleDoorWE
        }
        door_dict[door_name](game, x, y)


class DoorCon(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = self.game.map_rect[3]
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, self.game.closed_doors)

        self.subtype = "door"

    def open(self):
        # TODO: add a notifier state or rect to display door interaction message.
        self.kill()
        self.add(self.game.opened_doors, self.game.all_sprites)
        self.image = self.opened_img


class WoodenDoor(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game, x, y)

        self.closed_img = self.game.dcss1.image_at(23, 11, 1, 1)
        self.opened_img = self.game.dcss1.image_at(27, 11, 1, 1)

        self.imgrect_topleft(self.closed_img)

        self.name = "Wooden Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"


class WoodenDoubleDoorNS(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game, x, y)

        self.closed_img = self.game.dcss1.image_at(45, 11, 2, 1)
        self.opened_img = self.game.dcss1.image_at(48, 11, 2, 1)

        self.imgrect_topleft(self.closed_img)

        self.name = "Wooden Double Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"


class WoodenDoubleDoorWE(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game, x, y)

        self.closed_img = self.game.dcss2.image_at(31, 0, 1, 2)
        self.opened_img = self.game.dcss2.image_at(34, 0, 1, 2)

        self.imgrect_topleft(self.closed_img)

        self.name = "Wooden Double Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"
