import pygame as pg
from src.utils import Spritesheet
from .sprite import Sprite
from .items import Item
from src.states.notifywin import NotifyWin, NotifyChoiceWin


class InteractableCon(Sprite):
    def __init__(self, game, x, y, _):
        self._layer, self.adjustable_layer = -2, False
        super().__init__(game, x, y, game.interactables)
        self.spritesheet = game.other_sheet
        self.category = 'interactable'


class SwitchCon(InteractableCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.category = 'switch'
        self.event = False
        self.flagged_npc = None
        self.flagged_desc = None

        if props:
            if 'event' in props:
                self.event = True
                self.flagged_npc = props['flagged_npc']
                self.flagged_desc = props['flagged_desc']

            if 'crystal_type' in props:
                self.crystal_type = props['crystal_type']


class CrystalSwitch(SwitchCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.crystal_type == 'green':
            self.active_img = self.spritesheet.image_at(6, 3, 1, 1)
        elif self.crystal_type == 'red':
            self.active_img = self.spritesheet.image_at(7, 3, 1, 1)
        self.inert_img = self.spritesheet.image_at(5, 3, 1, 1)
        self.imgrect_topleft(self.active_img)
        self.name = 'Crystal Switch'
        self.active = True

    def interact(self):
        if self.active:
            NotifyChoiceWin(self.game, self.name,
                            'Do nothing', 'Touch it', 0, 1,
                            f"{self.crystal_type.capitalize()} energy swirls within this crystal").enter_state()
        else:
            NotifyWin(self.game, 1, 'The crystal is powerless.').enter_state()


class PortalCon(InteractableCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.category = 'portal'
        self.indentifier = None
        self.target = None
        self.charges = None
        self.prompt = False

        if props:
            if 'identifier' in props:
                self.identifier = props['identifier']

            if 'target' in props:
                self.target = props['target']

            if 'charges' in props:
                self.charges = props['charges']

            if 'prompt' in props:
                self.prompt = True

    def teleport(self):
        touched = pg.sprite.spritecollide(self.game.player.sprite, self.game.interactables, False)[-1]
        for interactable in self.game.interactables:
            if interactable.category == 'portal' and interactable.identifier == touched.target:
                self.game.player.sprite.rect.center = interactable.rect.center
                break


class TelePortal(PortalCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.imgrect_topleft(self.spritesheet.image_at(5, 4, 1, 1))
        self.name = 'Tele Portal'

    def interact(self):
        if self.prompt:
            NotifyChoiceWin(self.game, self.name,
                            'Do nothing', 'Reach in', 0, 1,
                            'A dark, swirling mass.').enter_state()
        else:
            touched = pg.sprite.spritecollide(self.game.player.sprite, self.game.interactables, False)[-1]
            for interactable in self.game.interactables:
                if interactable.category == 'portal' and interactable.identifier == touched.target:
                    self.game.player.sprite.rect.center = interactable.rect.center
                    break


class MapPortal(PortalCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)


class ScriptCon(InteractableCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.category = 'script'
        self.variance = 0
        self.step = 0


class SpaceScript(ScriptCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.imgrect_topleft(self.spritesheet.image_at(7, 0, 1, 1))
        self.name = 'Space Script'


class ChestCon(InteractableCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.category = 'chest'
        self.opened = False
        self.key_req = None
        self.contents = []

        if props:
            if 'contents' in props:
                self.contents = props['contents'].split(", ")

            if 'key_req' in props:
                self.key_req = props['key_req']
                self.desc = f"It's locked with {self.key_req.split()[0].lower()}"

            if 'opened' in props:
                self.opened = props['opened']

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
                for itemname in self.contents[:]:
                    Item(self.game, self.game.cleaner.sprite.x, self.game.cleaner.sprite.y, itemname)
                    item = pg.sprite.spritecollide(self.game.cleaner.sprite, self.game.items, True)[0]
                    notices.append(f"Found {item.name}.")

                    if len(self.game.player.sprite.inventory) < self.game.player.sprite.inventory_size:
                        self.game.player.sprite.inventory.append(item)
                        self.contents.remove(itemname)
                        notices.append(f"{item.name} added to inventory.")
                    else:
                        notices.append(f"Inventory full, can't take the {item.name}.")
                        break

                NotifyWin(self.game, 1, *notices).enter_state()

            else:
                notices.append("It's empty.")
                NotifyWin(self.game, 1, *notices).enter_state()


class WoodenChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 0, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 0, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = 'Wooden Chest'


class IronChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 1, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 1, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = 'Iron Chest'


class CoffinChest(ChestCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.spritesheet.image_at(5, 2, 1, 1)
        self.opened_img = self.spritesheet.image_at(6, 2, 1, 1)
        self.imgrect_topleft(self.closed_img if not self.opened else self.opened_img)
        self.name = 'Coffin'


class Interactable:
    interactable_dict = {
        'Crystal Switch': CrystalSwitch,
        'Map Portal': MapPortal,
        'Tele Portal': TelePortal,
        'Space Script': SpaceScript,
        'Wooden Chest': WoodenChest,
        'Iron Chest': IronChest,
        'Coffin Chest': CoffinChest
    }

    def __init__(self, game, x, y, interactable_name, props):
        self.interactable_dict[interactable_name](game, x, y, props)
