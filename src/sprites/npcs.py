import pygame as pg
from .sprite import Sprite
from .items import Item
from src.allocs.stats import Stats
from src.states.dialoguewin import DialogueWin


class NPC:
    def __init__(self, game, x, y, npc_name):
        self.game = game

        npc_dict = {
            "Green Square": GreenSquare,
            "Yellow Square": YellowSquare,
            "Blue Square": BlueSquare
        }

        npc_dict[npc_name](game, x, y)


class NPCCon(Sprite, Stats):
    def __init__(self, game, x, y):
        self.game = game
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, game.npcs)

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

    def apply_inventory(self):
        for i, itemname in enumerate(self.inventory):
            Item(self.game, self.game.cleaner.sprite.x, self.game.cleaner.sprite.y, itemname)
            item = pg.sprite.spritecollide(self.game.cleaner.sprite, self.game.items, True)[0]
            self.inventory[i] = item

    def drop_item(self, name):
        for item in self.inventory:
            if item.name == name:
                self.inventory.remove(item)
                Item(self.game, self.game.player.sprite.rect.centerx, self.game.player.sprite.rect.centery, item.name)
                break

    def drop_all(self):
        for item in self.inventory:
            self.inventory.remove(item)
            Item(self.game, self.centerx, self.centery, item.name)

    def take_item(self, name):
        for item in self.game.player.sprite.inventory:
            if item.name == name:
                self.game.player.sprite.inventory.remove(item)
                self.inventory.append(item)
                break

    def interact(self):
        self.game.select_sound.play()
        DialogueWin(self.game, self).enter_state()

    def relocate(self, x, y):
        # TODO: create a Tiled object at the location an npc should relocate to, and send its position to this function
        self.rect.center = (x, y)


# Speaker type: only engages in dialogue
class GreenSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Green Square"

        self.inventory = []
        self.apply_inventory()


# Trader type: can open a trade window through dialogue
class YellowSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((150, 150, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Yellow Square"


# Combatant type: only engages in combat
class BlueSquare(NPCCon):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        # self.imgrect(self.spritesheet.image_at(4, 3, 1, 1))
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        self.image.fill((0, 0, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Blue Square"
