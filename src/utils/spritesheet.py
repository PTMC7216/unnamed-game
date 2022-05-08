import pygame as pg


class Spritesheet:
    def __init__(self, game, filename):
        self.game = game
        self.x = self.game.tilesize
        self.y = self.game.tilesize

        image_dir = f'./data/images/spritesheets/{filename}'
        self.sheet = pg.image.load(image_dir)

    def image_at(self, col, row, col_span, row_span, colorkey=(0, 0, 0)):
        """
        Returns an image from a spritesheet.

        :param col: Starting column
        :param row: Starting row
        :param col_span: The height of the image, in number of tiles
        :param row_span: The width of the image, in number of tiles
        :param colorkey: Color to be made transparent. Black if no arg is passed
        :return: Surface
        """
        rect = pg.Rect((col * self.x), (row * self.y), (col_span * self.x), (row_span * self.y))
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    def image_strip(self, col, row, col_span, row_span, strip_len, colorkey=(0, 0, 0)):
        """
        Returns a list of images from a spritesheet. Intended for animating purposes.

        :param col: Starting column
        :param row: Starting row
        :param col_span: The height of the image, in number of tiles
        :param row_span: The width of the image, in number of tiles
        :param strip_len: Number of images to append to the returned list
        :param colorkey: Color to be made transparent. Black if no arg is passed
        :return: list
        """
        return [self.image_at(col + x, row, col_span, row_span, colorkey) for x in range(strip_len)]
