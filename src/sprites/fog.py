import pygame as pg
from .sprite import Sprite


class Fog(Sprite):
    def __init__(self, game, x, y):
        self._layer, self.adjustable_layer = game.map_rect[3] + 1, False
        super().__init__(game, x, y, game.fog)

        img = pg.Surface((game.tilesize, game.tilesize)).convert()
        img.fill((0, 0, 0))
        img.set_colorkey((1, 1, 1))
        self.imgrect_topleft(img)

        self.name = 'fog'
    #     self.visible = False
    #     self.explored = False
    #
    # def in_los(self):
    #     self.visible = True
    #     self.explored = True
    #
    # def out_los(self):
    #     self.visible = False
    #
    # def update(self):
    #     if self.visible:
    #         self.image.set_alpha(0)
    #     elif self.explored:
    #         self.image.set_alpha(170)
