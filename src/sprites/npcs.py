import pygame as pg
from .sprite import Sprite
from .items import Item
from src.allocs.stats import Stats
from src.states.dialoguewin import DialogueWin
from src.states.notifywin import NotifyWin


class NPCCon(Sprite, Stats):
    def __init__(self, game, x, y):
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

        self.flags = []
        self.dialogue_section = "check"
        self.dialogue_counter = 0
        self.dialogue_memory = []

        self.inventory = []

        self.relocation = 0

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
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_topleft(self.spritesheet.image_at(2, 0, 1, 1))
        self.name = "Head"
        self.inventory = ["Blue Orb"]
        self.apply_inventory()


class Obelisk(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.imgrect_topleft(self.spritesheet.image_at(0, 4, 1, 1))
        self.name = "Obelisk"
        self.variance = 0
        self.step = 0

    def interact(self):
        strings = {0: ["An immaculate obelisk hovers silently atop a metal plate."],
                   1: ["Despite being suspended in the air, it appears perfectly motionless."],
                   2: ["You admire the obelisk.",
                       "It fills you with a deep curiosity."],
                   3: ["You scrutinize the obelisk.",
                       "Voices slowly begin to manifest in your mind."],
                   5: ["The voices are gone."],
                   6: ["The obelisk."]}

        if self.step == 4:
            DialogueWin(self.game, self).enter_state()
        elif self.step < len(strings.keys()) + 1:
            NotifyWin(self.game, 1, *strings.get(self.step)).enter_state()
            if self.step < len(strings.keys()):
                self.step += 1


class YellowTest(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((150, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = "Yellow Test"


class BlueTest(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 0, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = "Blue Test"

    #     self.base_time = 0
    #     self.vel = 1
    #
    # def update(self):
    #     current_time = pg.time.get_ticks()
    #     if current_time - self.base_time > 1000:
    #         self.base_time = current_time
    #         if self.vel == 1:
    #             self.vel = -1
    #         else:
    #             self.vel = 1
    #
    #     self.rect.x += self.vel


class NPC:
    npc_dict = {
        "Head": Head,
        "Obelisk": Obelisk,
        "Yellow Test": YellowTest,
        "Blue Test": BlueTest
    }

    def __init__(self, game, x, y, npc_name):
        self.game = game
        self.npc_dict[npc_name](game, x, y)
