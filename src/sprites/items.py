import pygame as pg
from .sprite import Sprite
from src.states.notifywin import NotifyWin


class ItemCon(Sprite):
    def __init__(self, game, x, y):
        self._layer, self.adjustable_layer = -1, False
        super().__init__(game, x, y, game.items)

        self.spritesheet = game.item_sheet

        self.category = "item"
        self.equipped = False
        self.equipable = False
        self.usable = False

    def pickup(self):
        self.game.player.sprite.inv_add(self)

    def use(self):
        if not self.usable:
            NotifyWin(self.game, 1, f"Can't use the {self.name}.").enter_state()

        else:
            if self.category == "consumable":
                pass

            elif self.category == "reusable":
                pass

            elif self.category == "key":
                if pg.sprite.spritecollide(**self.game.player.sprite.door_collision_kwargs):
                    self.__use_key("door", **self.game.player.sprite.door_collision_kwargs)
                elif pg.sprite.spritecollide(**self.game.player.sprite.interactable_collision_kwargs):
                    self.__use_key("chest", **self.game.player.sprite.interactable_collision_kwargs)
                else:
                    NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

            else:
                NotifyWin(self.game, 2, f"Used the {self.name}, but nothing happened.").enter_state()

    def __use_key(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]
        if obj.category == category:
            if obj.key_req == self.name:
                notice = f"Opened the {obj.name.lower()} with the {self.name.lower()}."
                NotifyWin(self.game, 4, notice).enter_state()
                obj.open()
            elif obj.key_req is None:
                NotifyWin(self.game, 2, f"The {obj.name.lower()} is already unlocked.").enter_state()
            elif obj.key_req != self.name:
                NotifyWin(self.game, 2, f"The {self.name.lower()} doesn't fit.").enter_state()
        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

    def equip(self):
        if not self.equipable:
            NotifyWin(self.game, 1, f"Can't equip the {self.name}.").enter_state()
        elif not self.equipped:
            if self.category == "weapon":
                self.game.player.sprite.hand[0] = self
            elif self.category == "armor":
                pass
            elif self.category == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()
            NotifyWin(self.game, 2, f"Equipped the {self.name}.").enter_state()
        else:
            NotifyWin(self.game, 1, f"The {self.name} is already equipped.").enter_state()

    def unequip(self):
        if self.equipped:
            if self.category == "weapon":
                for i, item in enumerate(self.game.player.sprite.hand):
                    if item == self:
                        self.game.player.sprite.hand[i] = "None"
            elif self.category == "armor":
                pass
            elif self.category == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()
            NotifyWin(self.game, 2, f"Unequipped the {self.name}.").enter_state()

    def examine(self):
        NotifyWin(self.game, 1, self.desc).enter_state()

    def drop(self):
        if self.equipped:
            if self.category == "weapon":
                for i, item in enumerate(self.game.player.sprite.hand):
                    if item == self:
                        self.game.player.sprite.hand[i] = ""
            elif self.category == "armor":
                pass
            elif self.category == "accessory":
                pass
            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()

        if self in self.game.player.sprite.inventory:
            self.game.player.sprite.inventory.remove(self)

        for i, name in enumerate(self.game.state_stack):
            if repr(name) == "Inventory Window":
                self.game.state_stack[i].refresh()
                break

        NotifyWin(self.game, 2, f"Dropped the {self.name}.").enter_state()
        Item(self.game, self.game.player.sprite.rect.centerx, self.game.player.sprite.rect.centery, self.name)


class ConsumableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "consumable"
        self.equipable = False
        self.usable = True


class ReusableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "reusable"
        self.equipable = False
        self.usable = True


class WeaponCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "weapon"
        self.equipable = True
        self.usable = False


class ArmorCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "armor"
        self.equipable = True
        self.usable = False


class AccessoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "accessory"
        self.equipable = True
        self.usable = False


class KeyCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "key"
        self.equipable = False
        self.usable = True


class StoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = "story"
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

        self.imgrect_center(self.spritesheet.image_at(0, 3, 1, 1))
        self.name = "Brass Key"
        self.desc = "An ordinary brass key."


class IronKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.imgrect_center(self.spritesheet.image_at(0, 4, 1, 1))
        self.name = "Iron Key"
        self.desc = "A heavy iron key."


class Item:
    item_dict = {
        "Brass Key": BrassKey,
        "Iron Key": IronKey,
        "Rusted Sword": RustedSword
    }

    def __init__(self, game, x, y, item_name):
        self.item_dict[item_name](game, x, y)
