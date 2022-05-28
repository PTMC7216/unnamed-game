import pygame as pg
from .sprite import Sprite
from src.states.notifywin import NotifyWin


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
        self.equipped = False
        self.equipable = False
        self.usable = False

    def pickup(self):
        self.game.player.sprite.inv_add(self)

    def use(self):
        if not self.usable:
            notice = f"Can't use the {self.name}."
            NotifyWin(self.game, 1, notice).enter_state()
        else:
            if self.subtype == "consumable":
                pass

            elif self.subtype == "reusable":
                pass

            elif self.subtype == "key":
                kwargs = {"sprite": self.game.player.sprite, "group": self.game.closed_doors,
                          "dokill": False, "collided": pg.sprite.collide_rect_ratio(1.1)}
                if pg.sprite.spritecollide(**kwargs):
                    door = pg.sprite.spritecollide(**kwargs)[-1]
                    if door.key_req == self.name:
                        notice = f"Opened the {door.name.lower()} with the {self.name.lower()}."
                        NotifyWin(self.game, 4, notice).enter_state()
                        door.open()
                    elif door.key_req != self.name:
                        notice = f"The {self.name.lower()} doesn't fit."
                        NotifyWin(self.game, 2, notice).enter_state()
                else:
                    notice = f"Nothing to use the {self.name.lower()} on."
                    NotifyWin(self.game, 1, notice).enter_state()

            else:
                notice = f"Used the {self.name}, but nothing happened."
                NotifyWin(self.game, 2, notice).enter_state()

    def equip(self):
        if not self.equipable:
            notice = f"Can't equip the {self.name}."
            NotifyWin(self.game, 1, notice).enter_state()
        elif not self.equipped:
            if self.subtype == "weapon":
                self.game.player.sprite.hand[0] = self
            elif self.subtype == "armor":
                pass
            elif self.subtype == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()
            notice = f"Equipped the {self.name}."
            NotifyWin(self.game, 2, notice).enter_state()
        else:
            notice = f"The {self.name} is already equipped."
            NotifyWin(self.game, 1, notice).enter_state()

    def unequip(self):
        if self.equipped:
            if self.subtype == "weapon":
                for i, item in enumerate(self.game.player.sprite.hand):
                    if item == self:
                        self.game.player.sprite.hand[i] = ""
            elif self.subtype == "armor":
                pass
            elif self.subtype == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()
            notice = f"Unequipped the {self.name}."
            NotifyWin(self.game, 2, notice).enter_state()

    def examine(self):
        notice = self.desc
        NotifyWin(self.game, 1, notice).enter_state()

    def drop(self):
        if self.equipped:
            if self.subtype == "weapon":
                for i, item in enumerate(self.game.player.sprite.hand):
                    if item == self:
                        self.game.player.sprite.hand[i] = ""
            elif self.subtype == "armor":
                pass
            elif self.subtype == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()

        if self in self.game.player.sprite.inventory:
            self.game.player.sprite.inventory.remove(self)

        for i, name in enumerate(self.game.state_stack):
            if repr(name) == "Inventory Window":
                self.game.state_stack[i].refresh()
                break

        notice = f"Dropped the {self.name}."
        NotifyWin(self.game, 2, notice).enter_state()
        Item(self.game, self.game.player.sprite.rect.centerx, self.game.player.sprite.rect.centery, self.name)


class ConsumableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "consumable"
        self.equipable = False
        self.usable = True


class ReusableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "reusable"
        self.equipable = False
        self.usable = True


class WeaponCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "weapon"
        self.equipable = True
        self.usable = False


class ArmorCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "armor"
        self.equipable = True
        self.usable = False


class AccessoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "accessory"
        self.equipable = True
        self.usable = False


class KeyCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "key"
        self.equipable = False
        self.usable = True


class StoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.subtype = "story"
        self.equipable = False
        self.usable = False


class RustedSword(WeaponCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.damage = 1

        self.imgrect_center(self.spritesheet.image_at(0, 7, 1, 1))
        self.name = "Rusted Sword"
        self.desc = f"A rusty sword.\n" \
                    f"Damage: {self.damage}"


class BrassKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.imgrect_center(self.spritesheet.image_at(4, 3, 1, 1))
        self.name = "Brass Key"
        self.desc = "An ordinary brass key."
