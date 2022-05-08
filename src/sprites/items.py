import pygame as pg
from .sprite import Sprite


class Item:
    def __init__(self, game, x, y, item_name):
        item_dict = {
            "Brass Key": BrassKey,
            "Rusted Sword": RustedSword
        }
        item_dict[item_name](game, x, y)


class ItemCon(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = -1
        self.adjustable_layer = False
        Sprite.__init__(self, game, x, y, self.game.items)

        self.spritesheet = self.game.extra1

        self.subtype = "item"

    def pickup(self):
        # TODO: add notifier state, or rect, to display pickup message
        self.kill()
        self.game.player.sprite.inventory.append(self)
        print(f"{self.name} added to inventory.")


class ConsumableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "consumable"


class KeyCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "key"


class WeaponCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "weapon"


class ArmorCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "armor"


class AccessoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "accessory"


class BrassKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.imgrect_center(self.spritesheet.image_at(4, 3, 1, 1))
        self.name = "Brass Key"
        self.desc = "An ordinary brass key."


class RustedSword(WeaponCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.imgrect_center(self.spritesheet.image_at(0, 7, 1, 1))
        self.name = "Rusted Sword"
        self.desc = "A rusty sword."

        self.damage = 2
