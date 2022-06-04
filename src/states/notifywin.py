import pygame as pg
import src.utils as utils
from .menu import Menu


class NotifyWin(Menu):
    def __init__(self, game, state_exits, *notices):
        super().__init__(game)
        self.game = game
        self.state_exits = state_exits
        self.notices = notices
        self.notice = 0

        self.name = "Notification Window"

        self.pad = 20
        self.frame = self.framer.make_lower_frame(1.2, 3.6)
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, (0, 0, 0),
                                            topleft=(self.frame.x, self.frame.y))

        self.notification_pos = self.framer.set_pos(self.panel, self.pad)

        self.text_kwargs = {"width": self.panel["rect"].w - self.pad}

    def update(self):
        self.check_events()

        if self.keybind["z"] or self.keybind["x"] or self.keybind["esc"]:
            if len(self.notices) > 0 and self.notice < len(self.notices) - 1:
                self.game.select_sound.play()
                self.notice += 1
            else:
                self.game.select_sound.play()
                self.movement_key_check()
                self.exit_states(self.state_exits)

        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])
        utils.ptext.draw(self.notices[self.notice], (self.notification_pos["x"], self.notification_pos["y"]),
                         **self.text_kwargs)


class NotifyChoiceWin(NotifyWin):
    """c1 & c2 tuple layout: ('choice', 'flag')"""
    def __init__(self, game, category, c1: tuple, c2: tuple, state_exits, *notices):
        super().__init__(game, state_exits, *notices)

        self.category = category
        self.c1_str = c1[0]
        self.c1_flag = c1[1]
        self.c2_str = c2[0]
        self.c2_flag = c2[1]

        self.c_pos = self.framer.set_pos(self.panel, self.pad, y=80)
        self.c_index = 0
        self.c_spacing = 30

        self.position_selector(self.c_pos, -14, -2)

        self.selecting = False
        self.choice = self.c1_str
        self.flag = None

    def update(self):
        self.check_events()

        if self.notice >= len(self.notices) - 1:
            self.selecting = True

        if self.selecting:
            if self.keybind["up"] or self.keybind["down"]:
                self.game.selector_sound.play()
                if self.choice == self.c1_str:
                    self.choice = self.c2_str
                    self.c_index = 1
                else:
                    self.choice = self.c1_str
                    self.c_index = 0
                self.selector_rect.centery = (self.c_pos["y"] + self.selector_offset["y"]) + \
                                             (self.c_index * self.c_spacing)

        if self.keybind["z"]:
            if len(self.notices) > 0 and self.notice < len(self.notices) - 1:
                self.game.select_sound.play()
                self.notice += 1
            else:
                if self.c_index == 0:
                    self.flag = self.c1_flag
                elif self.c_index == 1:
                    self.flag = self.c2_flag
                self.flag_handler()

        if self.keybind["x"]:
            if len(self.notices) > 0 and self.notice < len(self.notices) - 1:
                self.game.select_sound.play()
                self.notice += 1
            else:
                self.game.select_sound.play()

        if self.keybind["esc"]:
            self.game.select_sound.play()
            self.movement_key_check()
            self.exit_states(self.state_exits)

        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])
        utils.ptext.draw(self.notices[self.notice], (self.notification_pos["x"], self.notification_pos["y"]),
                         **self.text_kwargs)

        if self.selecting:
            utils.ptext.draw(self.c1_str, (self.c_pos["x"], self.c_pos["y"]), **self.text_kwargs)
            utils.ptext.draw(self.c2_str, (self.c_pos["x"], self.c_pos["y"] + 30), **self.text_kwargs)
            utils.ptext.draw(">", self.selector_rect.center)

    def flag_handler(self):
        if self.category == "Pause Window":
            if self.flag == "Quit":
                pg.mixer.music.load('./data/music/ominous1.ogg')
                pg.mixer.music.play(-1, 0.0, 10000)
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()
            elif self.flag == "Return":
                self.game.select_sound.play()
                self.movement_key_check()
                self.exit_states(self.state_exits)
