import pygame as pg
import src.utils as utils
from .menu import Menu
from .inventorywin import InventoryWin
from .statuswin import StatusWin


class PauseWin(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.name = "Pause Window"

        self.frame = self.framer.make_center_frame(3, 2)
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h,
                                            topleft=(self.frame.x, self.frame.y))

        self.pos_adj = {"x": self.panel["rect"].w // 2,
                        "y": self.panel["rect"].h // 4}

        self.title_pos = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"])
        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 50)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 90)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 130)
        self.pos3 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 170)

        self.position_selector(self.pos0, -90, -2)

        self.choices = ["Resume", "Inventory", "Status", "Quit"]
        self.index_spacing = 40

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybind["x"]:
            self.game.select_sound.play()
            self.movement_key_check()
            self.exit_state()
        elif self.keybind["esc"]:
            self.game.select_sound.play()
            self.movement_key_check()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.prev_state.render()
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])

        utils.ptext.draw("PAUSED", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw(self.choices[0], center=(self.pos0["x"], self.pos0["y"]))
        utils.ptext.draw(self.choices[1], center=(self.pos1["x"], self.pos1["y"]))
        utils.ptext.draw(self.choices[2], center=(self.pos2["x"], self.pos2["y"]))
        utils.ptext.draw(self.choices[3], center=(self.pos3["x"], self.pos3["y"]))

        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == "Resume":
            self.movement_key_check()
            self.exit_state()

        elif self.choices[self.index] == "Inventory":
            InventoryWin(self.game).enter_state()

        elif self.choices[self.index] == "Status":
            StatusWin(self.game).enter_state()

        elif self.choices[self.index] == "Quit":
            pg.mixer.music.load('./data/music/ominous1.ogg')
            pg.mixer.music.play(-1, 0.0, 10000)
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
