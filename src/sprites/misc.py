import pygame as pg


class Obstacles(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        pg.sprite.Sprite.__init__(self, self.game.obstacles)

        self.rect = pg.Rect(x, y, w, h)
