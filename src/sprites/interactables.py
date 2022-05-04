import pygame as pg


class Interactable:
    def __init__(self, game, x, y, interactable_name):
        self.game = game

        interactable_dict = {
            "Wooden Chest": WoodenChest
        }

        interactable_dict[interactable_name](game, x, y)


class ChestCon(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = -2
        self.adjustable_layer = False
        pg.sprite.Sprite.__init__(self, self.game.interactables, self.game.all_sprites)
        self.ident = "chest"

    def open(self):
        self.image = self.opened_img


class WoodenChest(ChestCon):
    def __init__(self, game, x, y):
        ChestCon.__init__(self, game)

        self.closed_img = self.game.dcss1.image_at(44, 46, 1, 1)
        self.opened_img = self.game.dcss1.image_at(45, 46, 1, 1)

        self.image = self.closed_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.name = "Wooden Chest"

