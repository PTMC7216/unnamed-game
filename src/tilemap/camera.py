import pygame as pg


class Camera:
    def __init__(self, game):
        self.game = game

        self.width = self.game.map.width
        self.height = self.game.map.height
        self.rect = pg.Rect(0, 0, self.width, self.height)

    def apply_sprite(self, entity):
        return entity.rect.move(self.rect.topleft)

    def apply_rect(self, rect):
        return rect.move(self.rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.game.screen_res['x'] / 2)
        y = -target.rect.centery + int(self.game.screen_res['y'] / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - self.game.screen_res['x']), x)
        y = max(-(self.height - self.game.screen_res['y']), y)

        self.rect = pg.Rect(x, y, self.width, self.height)
