import pygame as pg
import src.utils as utils
from .menu import Menu


class PauseWin(Menu):
    def __init__(self, game):
        self.game = game
        Menu.__init__(self, game)

        self.title_pos = {"x": self.game.screen_res["x"] // 2,
                          "y": self.game.screen_res["y"] // 2 - 40}

        self.resume_pos = {"x": self.game.screen_res["x"] // 2,
                           "y": self.game.screen_res["y"] // 2 + 50}

        self.inventory_pos = {"x": self.game.screen_res["x"] // 2,
                              "y": self.game.screen_res["y"] // 2 + 90}

        self.status_pos = {"x": self.game.screen_res["x"] // 2,
                           "y": self.game.screen_res["y"] // 2 + 130}

        self.quit_pos = {"x": self.game.screen_res["x"] // 2,
                         "y": self.game.screen_res["y"] // 2 + 170}

        self.menu_options = ["Resume", "Inventory", "Status", "Quit"]
        self.index = 0

        self.selector_rect = pg.Rect(0, 0, 20, 20)
        self.selector_offset = {"x": -90, "y": -2}
        self.selector_rect.center = ((self.resume_pos["x"] + self.selector_offset["x"]),
                                     (self.resume_pos["y"] + self.selector_offset["y"]))

    def draw_selector(self):
        utils.ptext.draw(">",
                         center=self.selector_rect.center,
                         owidth=1,
                         ocolor=(0, 0, 0))

    def move_selector(self):
        if self.keybind["up"]:
            self.game.selector_sound.play()
            self.index = (self.index - 1) % len(self.menu_options)
            self.selector_rect.centery = (self.resume_pos["y"] + self.selector_offset["y"]) + (self.index * 40)

        elif self.keybind["down"]:
            self.game.selector_sound.play()
            self.index = (self.index + 1) % len(self.menu_options)
            self.selector_rect.centery = (self.resume_pos["y"] + self.selector_offset["y"]) + (self.index * 40)

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
            self.movement_key_check()
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.prev_state.render()
        # self.game.screen.blit(surface, position)  # TODO: blit a backdrop

        utils.ptext.draw("PAUSED",
                         center=(self.title_pos["x"], self.title_pos["y"]),
                         owidth=1,
                         ocolor=(0, 0, 0))

        utils.ptext.draw("Resume",
                         center=(self.resume_pos["x"], self.resume_pos["y"]),
                         owidth=1,
                         ocolor=(0, 0, 0))

        utils.ptext.draw("Inventory",
                         center=(self.inventory_pos["x"], self.inventory_pos["y"]),
                         owidth=1,
                         ocolor=(0, 0, 0))

        utils.ptext.draw("Status",
                         center=(self.status_pos["x"], self.status_pos["y"]),
                         owidth=1,
                         ocolor=(0, 0, 0))

        utils.ptext.draw("Quit",
                         center=(self.quit_pos["x"], self.quit_pos["y"]),
                         owidth=1,
                         ocolor=(0, 0, 0))

        self.draw_selector()

    def transition_state(self):
        if self.menu_options[self.index] == "Resume":
            self.movement_key_check()
            self.exit_state()

        elif self.menu_options[self.index] == "Inventory":
            for item in self.game.player.sprite.inventory:
                print(item.name)

        elif self.menu_options[self.index] == "Status":
            pass

        elif self.menu_options[self.index] == "Quit":
            pg.mixer.music.load('./data/music/ominous1.ogg')
            pg.mixer.music.play(-1, 0.0, 10000)
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
