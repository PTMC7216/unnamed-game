import pygame as pg
import operator
import math
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
        self.droppable = True

    def pickup(self):
        self.game.player.sprite.inv_add(self)

    def destroy(self):
        self.kill()
        self.game.player.sprite.inv_remove(self)
        self.game.player.sprite.inv_refresh()

    def _use_key(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category and not obj.opened:
            if obj.key_req == self.name:
                NotifyWin(self.game, 4, f"Opened the {obj.name.lower()} with the {self.name.lower()}.").enter_state()
                obj.open()

            elif obj.key_req != self.name:
                NotifyWin(self.game, 2, f"The {self.name.lower()} doesn't fit.").enter_state()

        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()

    def _use_orb(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category:
            if obj.rune_type == self.orb_type or self.orb_type == 'all':
                notices = [f"The runes fade away and the {obj.name.split()[-1].lower()} swings open."]
                self.charges -= 1
                if self.charges <= 0:
                    notices.append(f"The {self.name.lower()} shatters.")
                    self.destroy()
                NotifyWin(self.game, 4, *notices).enter_state()
                obj.open()

            elif obj.rune_type is None:
                notice = f"There are no runes sealing this {obj.name.split()[-1].lower()}."
                NotifyWin(self.game, 2, notice).enter_state()

            elif obj.rune_type != self.orb_type:
                notice = f"The {obj.rune_type} runes fail to react to the orb."
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
                player.update_stats()
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
                self.game.player.sprite.update_stats()
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
            self.game.player.sprite.update_stats()

        self.game.player.sprite.inv_remove(self)
        self.game.player.sprite.inv_refresh()

        NotifyWin(self.game, 2, f"Dropped the {self.name}.").enter_state()
        Item(self.game, self.game.player.sprite.rect.centerx, self.game.player.sprite.rect.centery, repr(self))


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


class OldBones(ArmorCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(2, 0, 1, 1))
        self.name = 'Old Bones'
        self.desc = 'A pair of strangely shaped bones.'
        self.equipable = False


class AccessoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'accessory'
        self.equipable = True
        self.usable = False


class MossyRing(AccessoryCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(2, 1, 1, 1))
        self.name = 'Mossy Ring'
        self.desc = 'This ring is covered with a thick layer of moss.'

    def examine(self):
        # Get player and altar xy tuples
        a, b = self.game.player.sprite.rect.center, (0, 0)
        for npc in self.game.npcs:
            if npc.name == 'Altar':
                b = npc.rect.center
                break

        # Calculate distance
        dx = b[0] - a[0]
        dy = b[1] - a[1]

        # Check distance
        if math.hypot(dx, dy) < 120:
            self.desc = 'The ring is at rest.'
            NotifyWin(self.game, 1, self.desc).enter_state()
            return

        # Calculate angle
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        degs = math.degrees(rads)

        # Check angle
        def compass(deg):
            compass_points = {
                'east':      0 <= deg < 20 or 340 <= deg <= 360,
                'northeast': 20 <= deg < 70,
                'north':     70 <= deg < 110,
                'northwest': 110 <= deg < 160,
                'west':      160 <= deg < 200,
                'southwest': 200 <= deg < 250,
                'south':     250 <= deg < 290,
                'southeast': 290 <= deg < 340
            }
            for direction, angle in compass_points.items():
                if angle:
                    return f"The ring pulls to the {direction}."

        self.desc = compass(degs)
        NotifyWin(self.game, 1, self.desc).enter_state()


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


class FakeBrassKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 1, 1, 1))
        self.name = 'Brass Key'
        self.desc = 'A simple brass key?'

    def __repr__(self):
        return 'Fake Brass Key'

    def _use_key(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category and not obj.opened:
            if obj.key_req == self.name:
                NotifyWin(self.game, 4, 'The key disintegrates.').enter_state()
                self.destroy()

            elif obj.key_req != self.name:
                NotifyWin(self.game, 2, f"The {self.name.lower()} doesn't fit.").enter_state()

        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()


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
        self.desc = 'A pale blue key.'

    def _use_key(self, category, **collision_kwargs):
        obj = pg.sprite.spritecollide(**collision_kwargs)[-1]

        if obj.category == category and not obj.opened:
            if obj.key_req == self.name:
                NotifyWin(self.game, 4, f"Opened the {obj.name.lower()} with the {self.name.lower()}.",
                          f"The {self.name.lower()} fades out of existence.").enter_state()
                obj.open()
                self.destroy()

            elif obj.key_req != self.name:
                NotifyWin(self.game, 2, f"The {self.name.lower()} doesn't fit.").enter_state()

        else:
            NotifyWin(self.game, 1, f"Nothing to use the {self.name.lower()} on.").enter_state()


class GreenKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 4, 1, 1))
        self.name = 'Green Key'
        self.desc = 'A jagged green metal key.'


class RedKey(KeyCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(0, 5, 1, 1))
        self.name = 'Red Key'
        self.desc = 'A fine red metal key.'


class OrbCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'orb'
        self.equipable = False
        self.usable = True
        self.charges = 1


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
        self.charges = float('inf')
        self.name = 'Brilliant Orb'
        self.desc = 'The energy within this orb appears limitless. \n\n' \
                    'It shifts through every color in the visible spectrum.'


class StoryCon(ItemCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.category = 'story'
        self.equipable = False
        self.usable = False

    def use_action(self):
        raise NotImplementedError


class PoisonFlask(StoryCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_center(self.spritesheet.image_at(3, 0, 1, 1))
        self.name = 'Poison Flask'
        self.desc = 'A fuming black liquid is contained within the flask.'
        self.usable = True

    def use_action(self):
        NotifyChoiceWin(self.game, self, 'No', 'Yes', 0, 1,
                        'Drink from the flask?').enter_state()


class Item:
    item_dict = {
        'Rusted Sword': RustedSword,
        'Old Bones': OldBones,
        'Mossy Ring': MossyRing,
        'Rusted Key': RustedKey,
        'Brass Key': BrassKey,
        'Fake Brass Key': FakeBrassKey,
        'Iron Key': IronKey,
        'Magic Key': MagicKey,
        'Green Key': GreenKey,
        'Red Key': RedKey,
        'Blue Orb': BlueOrb,
        'Yellow Orb': YellowOrb,
        'Brilliant Orb': BrilliantOrb,
        'Poison Flask': PoisonFlask
    }

    def __init__(self, game, x, y, item_name):
        self.item_dict[item_name](game, x, y)
