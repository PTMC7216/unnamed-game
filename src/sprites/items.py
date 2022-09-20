import pygame as pg
from .sprite import Sprite
from src.states.notifywin import NotifyWin, NotifyChoiceWin


class ItemCon(Sprite):
    def __init__(self, game, x, y):
        self._layer, self.adjustable_layer = -1, False
        super().__init__(game, x, y, game.items)

        self.spritesheet = game.item_sheet

        self.category = 'item'
        self.equipped = False
        self.equipable = False
        self.usable = False

    def pickup(self):
        self.game.player.sprite.inv_add(self)

    def _use_key(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category:
            if obj.key_req == self.name:
                NotifyWin(self.game, 4, f"Opened the {obj.name.lower()} with the {self.name.lower()}.").enter_state()
                obj.open()

            elif obj.key_req is None:
                NotifyWin(self.game, 2, f"The {obj.name.lower()} is already unlocked.").enter_state()

            elif obj.key_req != self.name:
                NotifyWin(self.game, 2, f"The {self.name.lower()} doesn't fit.").enter_state()

        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

    def _use_orb(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category:
            if obj.rune_type == self.orb_type or self.orb_type == 'all':
                notice = f"The runes fade away and the {obj.name.split()[-1].lower()} swings open."
                NotifyWin(self.game, 4, notice).enter_state()
                obj.open()

            elif obj.rune_type != self.orb_type:
                notice = f"The {obj.rune_type} runes fail to react to the orb."
                NotifyWin(self.game, 2, notice).enter_state()

            elif obj.rune_type is None:
                notice = f"There are no runes sealing this {obj.name.split()[-1].lower()}."
                NotifyWin(self.game, 2, notice).enter_state()

        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

    def use(self):
        if not self.usable:
            NotifyWin(self.game, 1, f"Can't use the {self.name}.").enter_state()

        else:
            if self.category == 'consumable':
                pass

            elif self.category == 'reusable':
                pass

            elif self.category == 'key':
                if pg.sprite.spritecollide(**self.game.player.sprite.door_collision_kwargs):
                    self._use_key('door', **self.game.player.sprite.door_collision_kwargs)
                elif pg.sprite.spritecollide(**self.game.player.sprite.interactable_collision_kwargs):
                    self._use_key('chest', **self.game.player.sprite.interactable_collision_kwargs)
                else:
                    NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

            elif self.category == 'orb':
                if pg.sprite.spritecollide(**self.game.player.sprite.door_collision_kwargs):
                    self._use_orb('door', **self.game.player.sprite.door_collision_kwargs)
                else:
                    NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

            elif self.category == 'story':
                self.use_action()

            else:
                NotifyWin(self.game, 2, f"Used the {self.name}, but nothing happened.").enter_state()

    def equip(self):
        player = self.game.player.sprite

        if not self.equipped:
            update = False

            if self.category == 'weapon':
                if player.hand[0] == 'None':
                    player.hand[0] = self
                    update = True

            elif self.category == 'armor':
                pass

            elif self.category == 'accessory':
                if player.available_slot(player.accessory):
                    player.set_slot(player.accessory, 'None', self)
                    update = True

            if update:
                self.equipped = not self.equipped
                player.update_substats()
                player.inv_remove(self)
                player.inv_refresh()
                NotifyWin(self.game, 2, f"Equipped the {self.name}.").enter_state()
            else:
                NotifyWin(self.game, 2, f"Can't equip the {self.name}.\n\nEquipment slots are full.").enter_state()

        else:
            NotifyWin(self.game, 1, f"The {self.name} is already equipped.").enter_state()

    def unequip(self):
        if self.equipped:
            if len(self.game.player.sprite.inventory) < self.game.player.sprite.inventory_size:

                if self.category == 'weapon':
                    self.game.player.sprite.set_slot(self.game.player.sprite.hand, self, 'None')

                elif self.category == 'armor':
                    pass

                elif self.category == 'accessory':
                    self.game.player.sprite.set_slot(self.game.player.sprite.accessory, self, 'None')

                self.equipped = not self.equipped
                self.game.player.sprite.update_substats()
                self.game.player.sprite.inv_add(self, notify=False)
                self.game.player.sprite.inv_refresh()
                NotifyWin(self.game, 2, f"Unequipped the {self.name}.").enter_state()

            else:
                NotifyWin(self.game, 2, f"Inventory full. Can't unequip.").enter_state()

    def examine(self):
        NotifyWin(self.game, 1, self.desc).enter_state()

    def drop(self):
        if self.equipped:

            if self.category == 'weapon':
                self.game.player.sprite.set_slot(self.game.player.sprite.hand, self, 'None')

            elif self.category == 'armor':
                pass

            elif self.category == 'accessory':
                self.game.player.sprite.set_slot(self.game.player.sprite.accessory, self, 'None')

            self.equipped = not self.equipped
            self.game.player.sprite.update_substats()

        self.game.player.sprite.inv_remove(self)
        self.game.player.sprite.inv_refresh()

        NotifyWin(self.game, 2, f"Dropped the {self.name}.").enter_state()
        Item(self.game, self.game.player.sprite.rect.centerx, self.game.player.sprite.rect.centery, self.name)


class ConsumableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'consumable'
        self.equipable = False
        self.usable = True


class ReusableCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'reusable'
        self.equipable = False
        self.usable = True


class WeaponCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'weapon'
        self.equipable = True
        self.usable = False


class RustedSword(WeaponCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 7, 1, 1))
        self.damage = 1
        self.name = 'Rusted Sword'
        self.desc = f"A rusty sword.\n" \
                    f"Damage: {self.damage}"


class ArmorCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'armor'
        self.equipable = True
        self.usable = False


class AccessoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'accessory'
        self.equipable = True
        self.usable = False


class KeyCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'key'
        self.equipable = False
        self.usable = True


class RustedKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 0, 1, 1))
        self.name = 'Rusted Key'
        self.desc = 'A heavy key covered in rust.'


class BrassKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 1, 1, 1))
        self.name = 'Brass Key'
        self.desc = 'A simple brass key.'


class IronKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 2, 1, 1))
        self.name = 'Iron Key'
        self.desc = 'A heavy iron key.'


class MagicKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 3, 1, 1))
        self.name = 'Magic Key'
        self.desc = 'A faintly humming blue key. \n\n' \
                    'It feels unusually fragile.'
        # TODO: single-use


class AdamantiteKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 4, 1, 1))
        self.name = 'Adamantite Key'
        self.desc = 'A jagged green metal key.'


class AurichalcumKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 5, 1, 1))
        self.name = 'Aurichalcum Key'
        self.desc = 'A fine red metal key.'


class OrbCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'orb'
        self.equipable = False
        self.usable = True
        # TODO: orb charges


class BlueOrb(OrbCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(1, 2, 1, 1))
        self.orb_type = 'blue'
        self.name = 'Blue Orb'
        self.desc = 'A shining blue orb.'


class YellowOrb(OrbCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(1, 3, 1, 1))
        self.orb_type = 'yellow'
        self.name = 'Yellow Orb'
        self.desc = 'A shining yellow orb.'


class BrilliantOrb(OrbCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(1, 4, 1, 1))
        self.orb_type = 'all'
        self.name = 'Brilliant Orb'
        self.desc = 'The energy within this orb appears limitless. \n\n' \
                    'It continuously shifts through every color in the visible spectrum.'


class StoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'story'
        self.equipable = False
        self.usable = False

    def use_action(self):
        raise NotImplementedError

class Item:
    item_dict = {
        'Rusted Key': RustedKey,
        'Brass Key': BrassKey,
        'Iron Key': IronKey,
        'Magic Key': MagicKey,
        'Adamantite Key': AdamantiteKey,
        'Aurichalcum Key': AurichalcumKey,
        'Blue Orb': BlueOrb,
        'Yellow Orb': YellowOrb,
        'Brilliant Orb': BrilliantOrb,
        'Rusted Sword': RustedSword
    }

    def __init__(self, game, x, y, item_name):
        self.item_dict[item_name](game, x, y)
