import pygame as pg


class Spritesheet:
    def __init__(self, game, filename):
        self.game = game
        self.x = self.game.tilesize
        self.y = self.game.tilesize

        image_dir = f'./data/images/spritesheets/{filename}'
        self.sheet = pg.image.load(image_dir)

    def image_at(self, col, row, col_span, row_span, colorkey=(0, 0, 0)):
        rect = pg.Rect((col * self.x), (row * self.y), (col_span * self.x), (row_span * self.y))
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    def image_strip(self, col, row, col_span, row_span, strip_len, colorkey=(0, 0, 0)):
        return [self.image_at(col + x, row, col_span, row_span, colorkey) for x in range(strip_len)]
