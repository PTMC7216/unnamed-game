import pygame as pg


class Door:
    def __init__(self, game, x, y, door_name):
        self.game = game

        door_dict = {
            "Wooden Door": WoodenDoor,
            "Wooden Double Door NS": WoodenDoubleDoorNS,
            "Wooden Double Door WE": WoodenDoubleDoorWE
        }

        door_dict[door_name](game, x, y)


class DoorCon(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = self.game.map_rect[3]
        self.adjustable_layer = True
        pg.sprite.Sprite.__init__(self, self.game.closed_doors, self.game.all_sprites)

    def open(self):
        self.kill()
        pg.sprite.Sprite.__init__(self, self.game.open_doors, self.game.all_sprites)
        self.image = self.opened_img

        # TODO: add a notifier state, or rect, to display door interaction message.
        #   include it in each door's open method, or player's open_door method.


class WoodenDoor(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game)

        self.closed_img = self.game.dcss1.image_at(23, 11, 1, 1)
        self.opened_img = self.game.dcss1.image_at(27, 11, 1, 1)

        self.image = self.closed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.name = "Wooden Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"


class WoodenDoubleDoorNS(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game)

        self.closed_img = self.game.dcss1.image_at(45, 11, 2, 1)
        self.opened_img = self.game.dcss1.image_at(48, 11, 2, 1)

        self.image = self.closed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.name = "Wooden Double Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"


class WoodenDoubleDoorWE(DoorCon):
    def __init__(self, game, x, y):
        DoorCon.__init__(self, game)

        self.closed_img = self.game.dcss2.image_at(31, 0, 1, 2)
        self.opened_img = self.game.dcss2.image_at(34, 0, 1, 2)

        self.image = self.closed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.name = "Wooden Double Door"
        self.desc = "This door is locked with brass."
        self.key_req = "Brass Key"
