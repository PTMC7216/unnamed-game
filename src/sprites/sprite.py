import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, spritegroup):
        self.game, self.x, self.y = game, x, y
        pg.sprite.Sprite.__init__(self, spritegroup, self.game.all_sprites)

    def __imgrect(self, img):
        self.image = img
        self.rect = self.image.get_rect()

    def imgrect_center(self, img):
        self.__imgrect(img)
        self.rect.center = (self.x, self.y)

    def imgrect_topleft(self, img):
        self.__imgrect(img)
        self.rect.topleft = (self.x, self.y)

    def __repr__(self):
        return self.name
