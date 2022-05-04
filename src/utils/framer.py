import pygame as pg


class Framer:
    def __init__(self, game):
        self.game = game

    def make_centered_frame(self, divx, divy):
        width = self.game.screen_res["x"] // divx
        height = self.game.screen_res["y"] // divy
        posx = ((self.game.screen_res["x"]) - (self.game.screen_res["x"] // divx)) // 2
        posy = self.game.screen_res["y"] - height - posx
        return pg.Rect(posx, posy, width, height)
