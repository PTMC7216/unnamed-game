import pygame as pg
import src.utils as utils
from .menu import Menu
from .overworld import Overworld


class MainMenu(Menu):
    def __init__(self, game):
        self.game = game
        Menu.__init__(self, game)

        self.title_pos = {"x": self.game.screen_res["x"] // 2,
                          "y": self.game.screen_res["y"] // 2 - 40}

        self.start_pos = {"x": self.game.screen_res["x"] // 2,
                          "y": self.game.screen_res["y"] // 2 + 50}

        self.options_pos = {"x": self.game.screen_res["x"] // 2,
                            "y": self.game.screen_res["y"] // 2 + 90}

        self.credits_pos = {"x": self.game.screen_res["x"] // 2,
                            "y": self.game.screen_res["y"] // 2 + 130}

        self.quit_pos = {"x": self.game.screen_res["x"] // 2,
                         "y": self.game.screen_res["y"] // 2 + 170}

        self.menu_options = ["Start Game", "Options", "Credits", "Quit Game"]
        self.index = 0

        self.selector_rect = pg.Rect(0, 0, 20, 20)
        self.selector_offset = {"x": -90, "y": -2}
        self.selector_rect.center = ((self.start_pos["x"] + self.selector_offset["x"]),
                                     (self.start_pos["y"] + self.selector_offset["y"]))

    def draw_selector(self):
        utils.ptext.draw(">", center=self.selector_rect.center)

    def move_selector(self):
        if self.keybind["up"]:
            self.game.selector_sound.play()
            self.index = (self.index - 1) % len(self.menu_options)
            self.selector_rect.centery = (self.start_pos["y"] + self.selector_offset["y"]) + (self.index * 40)
        elif self.keybind["down"]:
            self.game.selector_sound.play()
            self.index = (self.index + 1) % len(self.menu_options)
            self.selector_rect.centery = (self.start_pos["y"] + self.selector_offset["y"]) + (self.index * 40)

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            self.transition_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.game.background, (0, 0))

        utils.ptext.draw("Main Menu", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw("Start Game", center=(self.start_pos["x"], self.start_pos["y"]))
        utils.ptext.draw("Options", center=(self.options_pos["x"], self.options_pos["y"]))
        utils.ptext.draw("Credits", center=(self.credits_pos["x"], self.credits_pos["y"]))
        utils.ptext.draw("Quit Game", center=(self.quit_pos["x"], self.quit_pos["y"]))

        self.draw_selector()

    def transition_state(self):
        if self.menu_options[self.index] == "Start Game":
            self.movement_key_check()
            Overworld(self.game).enter_state()

        elif self.menu_options[self.index] == "Options":
            OptionsMenu(self.game).enter_state()

        elif self.menu_options[self.index] == "Credits":
            CreditsMenu(self.game).enter_state()

        elif self.menu_options[self.index] == "Quit Game":
            self.game.active = False


class OptionsMenu(MainMenu):
    def __init__(self, game):
        self.game = game
        MainMenu.__init__(self, game)

        self.menu_options = ["Volume", "Controls"]
        self.index = 0

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybind["z"]:
            self.game.select_sound.play()
            pass
        elif self.keybind["x"]:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.game.background, (0, 0))

        utils.ptext.draw("Options", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw("Volume", center=(self.start_pos["x"], self.start_pos["y"]))
        utils.ptext.draw("Controls", center=(self.options_pos["x"], self.options_pos["y"]))

        self.draw_selector()

    def transition_state(self):
        if self.menu_options[self.index] == "Volume":
            pass
        elif self.menu_options[self.index] == "Controls":
            pass


class CreditsMenu(MainMenu):
    def __init__(self, game):
        MainMenu.__init__(self, game)

        self.menu_options = []
        self.index = 0

    def update(self):
        self.check_events()
        if self.keybind["x"]:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.game.background, (0, 0))

        utils.ptext.draw("Credits", center=(self.title_pos["x"], self.title_pos["y"]))

        utils.ptext.draw("tiles: crawl", center=(self.start_pos["x"], self.start_pos["y"]))
        utils.ptext.draw("ptext: cosmologicon", center=(self.options_pos["x"], self.options_pos["y"]))
        utils.ptext.draw("...", center=(self.credits_pos["x"], self.credits_pos["y"]))
