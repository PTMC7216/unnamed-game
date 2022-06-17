import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, spritegroup):
        self.game, self.x, self.y = game, x, y
        super().__init__(spritegroup, self.game.all_sprites)

    def __repr__(self):
        return self.name

    def __imgrect(self, img):
        self.image = img
        self.rect = self.image.get_rect()

    def imgrect_center(self, img):
        self.__imgrect(img)
        self.rect.center = (self.x, self.y)

    def imgrect_topleft(self, img):
        self.__imgrect(img)
        self.rect.topleft = (self.x, self.y)

    def set_flag(self, npc_name, flag_name):
        for npc in self.game.npcs.sprites():
            if npc.name == npc_name and flag_name not in npc.flags:
                npc.flags.append(flag_name)
                break
