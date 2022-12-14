import pygame as pg
from .sprite import Sprite
from src.states.notifywin import NotifyWin


class DoorCon(Sprite):
    def __init__(self, game, x, y, props):
        self._layer, self.adjustable_layer = game.map_rect[3], True
        super().__init__(game, x, y, game.closed_doors)
        self.category = 'door'
        self.key_req = None
        self.rune_type = None
        self.shielded = False
        self.jammed = False
        self.opened = False
        self.event = False
        self.flagged_npc = None
        self.flagged_desc = None

        self.descs = {'Rusted Key': 'The door is held shut by a rusted lock',
                      'Brass Key': 'The door is locked with brass',
                      'Iron Key': 'The door is locked with iron',
                      'Magic Key': 'The door is held shut by a pale blue lock',
                      'Green Key': 'The door is held shut by a green lock',
                      'Red Key': 'The door is held shut by a fine metal lock'}

        if props:
            if 'key_req' in props:
                self.key_req = props['key_req']
                self.desc = self.descs[props['key_req']]

            if 'shield_type' in props:
                self.shield_type = props['shield_type']
                self.desc = f"The door is shielded by a layer of {self.shield_type.lower()} energy"

            if 'rune_type' in props:
                self.rune_type = props['rune_type']
                self.desc = f"The door is sealed with a row of glowing {self.rune_type.lower()} runes"

            if 'orientation' in props:
                self.orientation = props['orientation']

            if 'jammed' in props:
                self.jammed = props['jammed']

            if 'opened' in props:
                self.opened = props['spawn_open']

            if 'event' in props:
                self.event = True
                self.flagged_npc = props['flagged_npc']
                self.flagged_desc = props['flagged_desc']

    def open(self):
        if self.event:
            self.set_flag(self.flagged_npc, self.flagged_desc)
        self.opened = True
        self.kill()
        self.add(self.game.opened_doors, self.game.all_sprites)
        self.image = self.opened_img

    def interact(self):
        if not self.opened:
            if self.jammed:
                NotifyWin(self.game, 1, 'The door is jammed.').enter_state()
            else:
                if self.shielded:
                    NotifyWin(self.game, 1, f"{self.desc}.").enter_state()
                elif self.key_req is None and self.rune_type is None:
                    self.open()
                    NotifyWin(self.game, 1, f"Opened the {self.name.lower()}.").enter_state()
                else:
                    NotifyWin(self.game, 1, f"{self.desc}.").enter_state()

    def check_opened(self):
        if self.opened:
            self.open()


class WoodenDoor(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.closed_img = self.game.other_sheet.image_at(0, 0, 1, 1)
        self.opened_img = self.game.other_sheet.image_at(0, 1, 1, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = 'Wooden Door'
        self.check_opened()


class WoodenGate(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.orientation == 'ns':
            self.closed_img = self.game.other_sheet.image_at(3, 0, 1, 2)
            self.opened_img = self.game.other_sheet.image_at(4, 0, 1, 2)
        elif self.orientation == 'we':
            self.closed_img = self.game.other_sheet.image_at(1, 0, 2, 1)
            self.opened_img = self.game.other_sheet.image_at(1, 1, 2, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = 'Wooden Gate'
        self.check_opened()


class RunedDoor(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.rune_type == 'blue':
            self.closed_img = self.game.other_sheet.image_at(0, 2, 1, 1)
        elif self.rune_type == 'yellow':
            self.closed_img = self.game.other_sheet.image_at(0, 4, 1, 1)
        self.opened_img = self.game.other_sheet.image_at(0, 1, 1, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = 'Runed Door'


class RunedGate(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.orientation == 'ns':
            if self.rune_type == 'blue':
                self.closed_img = self.game.other_sheet.image_at(3, 2, 1, 2)
            elif self.rune_type == 'yellow':
                self.closed_img = self.game.other_sheet.image_at(3, 4, 1, 2)
            self.opened_img = self.game.other_sheet.image_at(4, 0, 1, 2)

        elif self.orientation == 'we':
            if self.rune_type == 'blue':
                self.closed_img = self.game.other_sheet.image_at(1, 2, 2, 1)
            elif self.rune_type == 'yellow':
                self.closed_img = self.game.other_sheet.image_at(1, 4, 2, 1)
            self.opened_img = self.game.other_sheet.image_at(1, 1, 2, 1)

        self.imgrect_topleft(self.closed_img)
        self.name = 'Runed Gate'


class EnergyDoor(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.shield_type == 'green':
            self.closed_img = self.game.other_sheet.image_at(0, 3, 1, 1)
        elif self.shield_type == 'red':
            self.closed_img = self.game.other_sheet.image_at(0, 5, 1, 1)
        self.opened_img = self.game.other_sheet.image_at(0, 1, 1, 1)
        self.imgrect_topleft(self.closed_img)
        self.name = 'Energy Door'
        self.shielded = True


class EnergyGate(DoorCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        if self.orientation == 'ns':
            if self.shield_type == 'green':
                self.closed_img = self.game.other_sheet.image_at(4, 2, 1, 2)
            elif self.shield_type == 'red':
                self.closed_img = self.game.other_sheet.image_at(4, 4, 1, 2)
            self.opened_img = self.game.other_sheet.image_at(4, 0, 1, 2)

        elif self.orientation == 'we':
            if self.shield_type == 'green':
                self.closed_img = self.game.other_sheet.image_at(1, 3, 2, 1)
            elif self.shield_type == 'red':
                self.closed_img = self.game.other_sheet.image_at(1, 5, 2, 1)
            self.opened_img = self.game.other_sheet.image_at(1, 1, 2, 1)

        self.imgrect_topleft(self.closed_img)
        self.name = 'Energy Gate'
        self.shielded = True


class Door:
    door_dict = {
        'Wooden Door': WoodenDoor,
        'Wooden Gate': WoodenGate,
        'Runed Door': RunedDoor,
        'Runed Gate': RunedGate,
        'Energy Door': EnergyDoor,
        'Energy Gate': EnergyGate
    }

    def __init__(self, game, x, y, door_name, props):
        self.door_dict[door_name](game, x, y, props)
