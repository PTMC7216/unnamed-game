import pygame as pg
import src.utils as utils
from .state import State


class Menu(State):
    def __init__(self, game):
        super().__init__(game)

        self.framer = utils.Framer(self.game)

        self.c_spacing = 40
        self.selector_rect = pg.Rect(0, 0, 20, 20)
        self.selector_offset = {'x': -90, 'y': -2}

        self.choices = []
        self.index = 0

        self.keydown = None
        self.keybool = {
            'esc': False,
            'up': False,
            'down': False,
            'left': False,
            'right': False,
            'z': False,
            'x': False
        }

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.active = False

            if event.type == pg.KEYDOWN:
                self.keydown = pg.key.name(event.key)

                if event.key == pg.K_ESCAPE:
                    self.keybool['esc'] = True
                if event.key == self.game.control['up']:
                    self.keybool['up'] = True
                if event.key == self.game.control['down']:
                    self.keybool['down'] = True
                if event.key == self.game.control['left']:
                    self.keybool['left'] = True
                if event.key == self.game.control['right']:
                    self.keybool['right'] = True
                if event.key == self.game.control['select']:
                    self.keybool['z'] = True
                if event.key == self.game.control['back']:
                    self.keybool['x'] = True

    def key_reset(self):
        self.keybool['esc'] = False
        self.keybool['up'] = False
        self.keybool['down'] = False
        self.keybool['left'] = False
        self.keybool['right'] = False
        self.keybool['z'] = False
        self.keybool['x'] = False

    def movement_key_check(self):
        self.game.player.sprite.clear_stacks()
        if pg.key.get_pressed()[self.game.control['up']]:
            self.game.player.sprite.dy.insert(0, -self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'up')
        if pg.key.get_pressed()[self.game.control['down']]:
            self.game.player.sprite.dy.insert(0, self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, down)
        if pg.key.get_pressed()[self.game.control['left']]:
            self.game.player.sprite.dx.insert(0, -self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'left')
        if pg.key.get_pressed()[self.game.control['right']]:
            self.game.player.sprite.dx.insert(0, self.game.player.sprite.movespeed)
            self.game.player.sprite.direction.insert(0, 'right')

    def position_selector(self, pos, offx, offy):
        self.selector_offset = {'x': offx, 'y': offy}
        self.selector_rect.center = ((pos['x'] + self.selector_offset['x']),
                                     (pos['y'] + self.selector_offset['y']))

    def draw_selector(self, **kwargs):
        utils.ptext.draw('>', center=self.selector_rect.center, **kwargs)

    def move_selector(self):
        if self.keybool['up']:
            self.game.selector_sound.play()
            self.index = (self.index - 1) % len(self.choices)
            self.selector_rect.centery = (self.pos0['y'] + self.selector_offset['y']) + \
                                         (self.index * self.c_spacing)
        elif self.keybool['down']:
            self.game.selector_sound.play()
            self.index = (self.index + 1) % len(self.choices)
            self.selector_rect.centery = (self.pos0['y'] + self.selector_offset['y']) + \
                                         (self.index * self.c_spacing)
