import pygame as pg
from .sprite import Sprite


class Fog(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = self.game.map_rect[3] + 1
        self.adjustable_layer = False
        super().__init__(game, x, y, self.game.fog)

        self.name = "fog"

        img = pg.Surface((self.game.tilesize, self.game.tilesize)).convert()
        img.fill((0, 0, 0))
        img.set_colorkey((1, 1, 1))
        self.imgrect_topleft(img)
