import pygame as pg
import operator
import src.utils as utils
from .menu import Menu
from .overworld import Overworld


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.name = "Main Menu"

        self.frame = self.framer.make_center_frame()
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h,
                                            topleft=(self.frame.x, self.frame.y))

        self.pos_adj = {"x": self.panel["rect"].w // 2,
                        "y": self.panel["rect"].h // 2}

        self.title_pos = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] - 40)
        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 50)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 90)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 130)
        self.pos3 = self.framer.set_pos(self.panel, x=self.pos_adj["x"], y=self.pos_adj["y"] + 170)

        self.position_selector(self.pos0, -90, -2)

        self.choices = ["Start Game", "Options", "Credits", "Quit Game"]
        self.c_spacing = 40

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            self.transition_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])

        utils.ptext.draw("Main Menu", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw(self.choices[0], center=(self.pos0["x"], self.pos0["y"]))
        utils.ptext.draw(self.choices[1], center=(self.pos1["x"], self.pos1["y"]))
        utils.ptext.draw(self.choices[2], center=(self.pos2["x"], self.pos2["y"]))
        utils.ptext.draw(self.choices[3], center=(self.pos3["x"], self.pos3["y"]))

        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == "Start Game":
            self.movement_key_check()
            Overworld(self.game).enter_state()

        elif self.choices[self.index] == "Options":
            OptionsMenu(self.game).enter_state()

        elif self.choices[self.index] == "Credits":
            CreditsMenu(self.game).enter_state()

        elif self.choices[self.index] == "Quit Game":
            self.game.active = False


class OptionsMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.name = "Options Menu"

        self.choices = ["Audio", "Controls"]
        self.index = 0

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybind["x"]:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])

        utils.ptext.draw("Options", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw(self.choices[0], center=(self.pos0["x"], self.pos0["y"]))
        utils.ptext.draw(self.choices[1], center=(self.pos1["x"], self.pos1["y"]))

        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == "Audio":
            AudioMenu(self.game).enter_state()
        elif self.choices[self.index] == "Controls":
            pass  # TODO: Options: ControlsMenu


class AudioMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.name = "Audio Menu"

        self.choices = ["SFX", "BGM"]
        self.index = 0

    def adjust_volume(self, addsub):
        def adjust(x): return round(addsub(x, 0.1), 1)
        if self.choices[self.index] == "SFX":
            self.game.selector_sound.set_volume(adjust(self.game.selector_sound.get_volume()))
            self.game.select_sound.set_volume(adjust(self.game.selector_sound.get_volume()))
        elif self.choices[self.index] == "BGM":
            pg.mixer.music.set_volume(adjust(pg.mixer.music.get_volume()))

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybind["x"]:
            self.game.select_sound.play()
            self.exit_state()
        elif self.keybind["left"]:
            self.game.select_sound.play()
            self.adjust_volume(operator.sub)
        elif self.keybind["right"]:
            self.game.select_sound.play()
            self.adjust_volume(operator.add)
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])

        utils.ptext.draw("Audio", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw(self.choices[0], center=(self.pos0["x"] - 30, self.pos0["y"]))
        utils.ptext.draw(f"{round(self.game.selector_sound.get_volume(), 1)}",
                         center=(self.pos0["x"] + 30, self.pos0["y"]))

        utils.ptext.draw(self.choices[1], center=(self.pos1["x"] - 30, self.pos1["y"]))
        utils.ptext.draw(f"{round(pg.mixer.music.get_volume(), 1)}",
                         center=(self.pos1["x"] + 30, self.pos1["y"]))

        self.draw_selector()

    def transition_state(self):
        pass


class CreditsMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)

        self.name = "Credits Menu"

        self.choices = []
        self.index = 0

    def update(self):
        self.check_events()
        if self.keybind["x"]:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel["surf"], self.panel["rect"])

        utils.ptext.draw("Credits", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw("tiles: crawl", center=(self.pos0["x"], self.pos0["y"]))
        utils.ptext.draw("ptext: cosmologicon", center=(self.pos1["x"], self.pos1["y"]))
        utils.ptext.draw("...", center=(self.pos2["x"], self.pos2["y"]))
