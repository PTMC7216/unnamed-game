import pygame as pg
import src.utils as utils
from .menu import Menu


class NotifyWin(Menu):
    def __init__(self, game, notice, state_exits):
        super().__init__(game)
        self.game = game
        self.notice = notice
        self.state_exits = state_exits

        self.name = "Notification Window"

        self.pad = 20
        self.frame = self.framer.make_lower_frame(1.2, 3.6)
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, (0, 0, 0),
                                            topleft=(self.frame.x, self.frame.y))

        self.notification_pos = self.framer.set_pos(self.panel, self.pad)

        self.text_kwargs = {"width": self.panel["rect"].w - self.pad}

        # TODO: implement multi-page capabilities, akin to DialogueWin

    def update(self):
        self.check_events()
        if self.keybind["z"] or self.keybind["x"] or self.keybind["esc"]:
            self.game.select_sound.play()
            self.movement_key_check()
            self.exit_states(self.state_exits)

        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])
        utils.ptext.draw(self.notice, (self.notification_pos["x"], self.notification_pos["y"]), **self.text_kwargs)
