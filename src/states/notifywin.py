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

        # TODO: implement choices

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
