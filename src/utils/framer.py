import pygame as pg


class Framer:
    def __init__(self, game):
        self.game = game

    def make_upper_frame(self, divxy=1, divy=3):
        """
        Creates an empty Rect filling the entirety of the game screen.
        Arguments may be passed to shrink the Rect to the desired size.
        Shrinking will favor upper positioning.

        :param divxy: Shrinks Rect along the "x" axis and pulls down on the Rect's upper edge to match
        :param divy: Pulls up on the Rect's lower edge
        :return: Rect
        """
        width = self.game.screen_res["x"] // divxy
        height = self.game.screen_res["y"] // divy
        posx = ((self.game.screen_res["x"]) - (self.game.screen_res["x"] // divxy)) // 2
        posy = ((self.game.screen_res["y"]) - (self.game.screen_res["y"] // divxy)) // 2
        return pg.Rect(posx, posy, width, height)

    def make_center_frame(self, divx=1, divy=1):
        """
        Creates an empty Rect filling the entirety of the game screen.
        Arguments may be passed to shrink the Rect to the desired size.
        Shrinking will favor central positioning.

        :param divx: Shrinks Rect along the "x" axis
        :param divy: Shrinks Rect along the "y" axis
        :return: Rect
        """
        width = self.game.screen_res["x"] // divx
        height = self.game.screen_res["y"] // divy
        posx = ((self.game.screen_res["x"]) - (self.game.screen_res["x"] // divx)) // 2
        posy = ((self.game.screen_res["y"]) - (self.game.screen_res["y"] // divy)) // 2
        return pg.Rect(posx, posy, width, height)

    def make_lower_frame(self, divxy=1, divy=3):
        """
        Creates an empty Rect filling the entirety of the game screen.
        Arguments may be passed to shrink the Rect to the desired size.
        Shrinking will favor lower positioning.

        :param divxy: Shrinks Rect along the "x" axis and pulls up on the Rect's bottom edge to match
        :param divy: Pulls down on the Rect's upper edge
        :return: Rect
        """
        width = self.game.screen_res["x"] // divxy
        height = self.game.screen_res["y"] // divy
        posx = ((self.game.screen_res["x"]) - (self.game.screen_res["x"] // divxy)) // 2
        posy = self.game.screen_res["y"] - height - posx
        return pg.Rect(posx, posy, width, height)

    @staticmethod
    def make_panel(surfw, surfh, color=(0, 0, 0), **kwargs):
        """
        Creates a blank Surface of given width and height, and a Rect of the same size.

        :param surfw: Surface width
        :param surfh: Surface height
        :param color: Surface color
        :param kwargs: Rect kwargs. e.x. topleft=(x, y)
        :return: dict containing "surf", "rect" key value pairs
        """
        surf = pg.Surface((surfw, surfh)).convert()
        surf.fill(color)
        rect = surf.get_rect(**kwargs)
        return {"surf": surf, "rect": rect}

    @staticmethod
    def set_pos(panel, padding=0, x=0, y=0):
        """
        Sets a position for an object within a panel.
        Coordinates start at 0 on the panel's topleft corner.

        :param panel: Container panel
        :param padding: Space between the object and panel
        :param x: Position on the x-axis
        :param y: Position on the y-axis
        :return: dict containing "x", "y" key value pairs
        """
        return {"x": panel["rect"].x + padding + x,
                "y": panel["rect"].y + padding + y}

