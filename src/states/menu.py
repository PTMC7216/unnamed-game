import pygame as pg
from .state import State


class Menu(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

        self.keybind = {
            "esc": False,
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "z": False,
            "x": False
        }

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.active = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.keybind["esc"] = True
                if event.key == pg.K_UP:
                    self.keybind["up"] = True
                if event.key == pg.K_DOWN:
                    self.keybind["down"] = True
                if event.key == pg.K_LEFT:
                    self.keybind["left"] = True
                if event.key == pg.K_RIGHT:
                    self.keybind["right"] = True
                if event.key == pg.K_z:
                    self.keybind["z"] = True
                if event.key == pg.K_x:
                    self.keybind["x"] = True

    def key_reset(self):
        self.keybind["esc"] = False
        self.keybind["up"] = False
        self.keybind["down"] = False
        self.keybind["left"] = False
        self.keybind["right"] = False
        self.keybind["z"] = False
        self.keybind["x"] = False

    def movement_key_check(self):
        self.game.player.sprite.clear_stacks()
        if pg.key.get_pressed()[pg.K_UP]:
            self.game.player.sprite.dy.insert(0, -self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'up')
        if pg.key.get_pressed()[pg.K_DOWN]:
            self.game.player.sprite.dy.insert(0, self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'down')
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.game.player.sprite.dx.insert(0, -self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'left')
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.game.player.sprite.dx.insert(0, self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'right')
