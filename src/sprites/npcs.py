import pygame as pg
from .sprite import Sprite
from .items import Item
from src.allocs.stats import Stats
from src.states.dialoguewin import DialogueWin
from src.states.notifywin import NotifyWin


class NPCCon(Sprite, Stats):
    def __init__(self, game, x, y, props):
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, game.npcs)

        self.spritesheet = game.npc_sheet

        Stats.__init__(
            self,
            lv=1,
            hp=9,
            mp=0,
            strength=1,
            dexterity=1,
            agility=1,
            vitality=1,
            intelligence=1,
            charisma=1,
            alignment=5)

        self.variant = None

        self.flags = []
        self.dialogue_section = 'check'
        self.dialogue_counter = 0
        self.dialogue_memory = []

        self.inventory = []

        self.relocation = 0

        if props:
            if 'variant' in props:
                self.variant = props['variant']

    def apply_inventory(self):
        for i, itemname in enumerate(self.inventory):
            Item(self.game, self.game.cleaner.sprite.x, self.game.cleaner.sprite.y, itemname)
            item = pg.sprite.spritecollide(self.game.cleaner.sprite, self.game.items, True)[0]
            self.inventory[i] = item

    def drop_item(self, name):
        for item in self.inventory:
            if item.name == name:
                self.inventory.remove(item)
                Item(self.game, self.rect.centerx, self.rect.centery, item.name)
                break

    def drop_all(self):
        for item in self.inventory:
            self.inventory.remove(item)
            Item(self.game, self.rect.centerx, self.rect.centery, item.name)

    def take_item(self, name):
        for item in self.game.player.sprite.inventory:
            if item.name == name:
                self.game.player.sprite.inventory.remove(item)
                self.inventory.append(item)
                break

    def interact(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()

    def relocate(self):
        for relocator in self.game.relocators:
            if self.name in relocator.name:
                if self.relocation == relocator.relocation:
                    self.rect.center = (relocator.x, relocator.y)
                    break


class Head(NPCCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.imgrect_topleft(self.spritesheet.image_at(2, 0, 1, 1))
        self.name = 'Head'
        self.inventory = ['Blue Orb']
        self.apply_inventory()


class Obelisk(NPCCon):
    variants = {}
    variations = 5
    for x in range(variations):
        variants.update({x: f"Obelisk {x}"})

    strings = {0: ["An immaculate obelisk hovers silently atop a metal plate.",
                   "Despite being suspended in the air, it appears perfectly motionless."],
               1: ["You admire the obelisk."],
               2: ["Voices begin to manifest in your mind."],
               # 3: DialogueWin step
               4: ["The voices are gone."],
               5: ["The obelisk."]}

    step = 0

    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.imgrect_topleft(self.spritesheet.image_at(0, 4, 1, 1))
        self.name = 'Obelisk'
        if self.variant is not None:
            self.name = self.variants[self.variant]

    def interact(self):
        if self.step == 2:
            DialogueWin(self.game, self).enter_state()
            NotifyWin(self.game, 1, *self.strings.get(self.step)).enter_state()
            self.step += 1
        elif self.step < len(self.strings.keys()) + 1:
            NotifyWin(self.game, 1, *self.strings.get(self.step)).enter_state()

        if self.step < 2:
            Obelisk.step += 1
        elif self.step < len(self.strings.keys()):
            self.step += 1


class Altar(NPCCon):
    def __init__(self, game, x, y, props):
        super().__init__(game, x, y, props)
        self.imgrect_topleft(self.spritesheet.image_at(3, 0, 1, 1))
        self.name = 'Altar'


class NPC:
    npc_dict = {
        'Head': Head,
        'Obelisk': Obelisk,
        'Altar': Altar
    }

    def __init__(self, game, x, y, npc_name, props):
        self.game = game
        self.npc_dict[npc_name](game, x, y, props)
