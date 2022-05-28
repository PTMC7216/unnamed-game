import pygame as pg
import src.utils as utils
from src.states.menu import Menu


class StatusWin(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game

        self.name = "Status Window"

        self.frame = self.framer.make_center_frame(2, 1.93)
        self.gap = 10
        self.padding = 10

        self.c_panel = self.framer.make_panel((self.frame.w // 3) - self.gap, self.frame.h - 180,
                                              bottomleft=(self.frame.x + self.gap, (self.frame.y * 2) - 5 - self.gap),
                                              color=(100, 100, 100))
        self.c_adj = {"x": self.padding,
                      "y": self.padding - 2}
        self.c_name_pos = self.framer.set_pos(self.c_panel, x=self.c_adj["x"], y=self.c_adj["y"])
        self.c_title_pos = self.framer.set_pos(self.c_panel, x=self.c_adj["x"], y=self.c_adj["y"] + 30)
        self.c_hp_pos = self.framer.set_pos(self.c_panel, x=self.c_adj["x"], y=self.c_adj["y"] + 60)
        self.c_mp_pos = self.framer.set_pos(self.c_panel, x=self.c_adj["x"], y=self.c_adj["y"] + 90)

        self.s_panel = self.framer.make_panel((self.frame.w // 3) - self.gap, self.frame.h - 120,
                                              topleft=(self.frame.x + self.gap, (self.frame.y * 2) - 5),
                                              color=(100, 100, 100))
        self.s_adj = {"x": self.padding,
                      "y": self.padding + 10}
        self.pos0 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"])
        self.pos1 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"] + 30)
        self.pos2 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"] + 60)
        self.pos3 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"] + 90)
        self.pos4 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"] + 120)
        self.pos5 = self.framer.set_pos(self.s_panel, x=self.s_adj["x"], y=self.s_adj["y"] + 150)

        self.e_panel = self.framer.make_panel((self.frame.w // 1.5) - self.gap, self.frame.h + 20,
                                              topleft=((self.frame.w // 1.2) + self.gap, self.frame.y),
                                              color=(100, 100, 100))
        self.e_adj = {"x": self.padding,
                      "y": self.padding + 10}
        self.e_pos0 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"])
        self.e_pos1 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 30)
        self.e_pos2 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 60)
        self.e_pos3 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 90)
        self.e_pos4 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 120)
        self.e_pos5 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 150)
        self.e_pos6 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 180)
        self.e_pos7 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 210)
        self.e_pos8 = self.framer.set_pos(self.e_panel, x=self.e_adj["x"], y=self.e_adj["y"] + 240)

        self.position_selector(self.pos0, -15, -2)

        self.choices = ["STR: n/a", "DEX: n/a", "AGI: n/a", "INT: n/a", "CHA: n/a"]
        self.e_choices = ["Right Hand: n/a", "Left Hand: n/a",
                          "Accessory 1: n/a", "Accessory 2: n/a",
                          "Head: n/a", "Torso: n/a", "Gloves: n/a", "Legs: n/a", "Boots: n/a"]
        self.index_spacing = 30

        self.text_kwargs = {"fontsize": 35}

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
        self.game.screen.blit(self.c_panel["surf"], self.c_panel["rect"])
        self.game.screen.blit(self.s_panel["surf"], self.s_panel["rect"])
        self.game.screen.blit(self.e_panel["surf"], self.e_panel["rect"])

        utils.ptext.draw("Name",
                         topleft=(self.c_name_pos["x"], self.c_name_pos["y"]), **self.text_kwargs)

        utils.ptext.draw("Title",
                         topleft=(self.c_title_pos["x"], self.c_title_pos["y"]), **self.text_kwargs)

        utils.ptext.draw(f"HP: n/a",
                         topleft=(self.c_hp_pos["x"], self.c_hp_pos["y"]), **self.text_kwargs)

        utils.ptext.draw("MP: n/a",
                         topleft=(self.c_mp_pos["x"], self.c_mp_pos["y"]), **self.text_kwargs)

        utils.ptext.draw(self.choices[0], midleft=(self.pos0["x"], self.pos0["y"]), **self.text_kwargs)
        utils.ptext.draw(self.choices[1], midleft=(self.pos1["x"], self.pos1["y"]), **self.text_kwargs)
        utils.ptext.draw(self.choices[2], midleft=(self.pos2["x"], self.pos2["y"]), **self.text_kwargs)
        utils.ptext.draw(self.choices[3], midleft=(self.pos3["x"], self.pos3["y"]), **self.text_kwargs)
        utils.ptext.draw(self.choices[4], midleft=(self.pos4["x"], self.pos4["y"]), **self.text_kwargs)
        utils.ptext.draw("Unallocated: n/a", midleft=(self.pos5["x"], self.pos5["y"]), fontsize=20)

        utils.ptext.draw(self.e_choices[0], midleft=(self.e_pos0["x"], self.e_pos0["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[1], midleft=(self.e_pos1["x"], self.e_pos1["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[2], midleft=(self.e_pos2["x"], self.e_pos2["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[3], midleft=(self.e_pos3["x"], self.e_pos3["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[4], midleft=(self.e_pos4["x"], self.e_pos4["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[5], midleft=(self.e_pos5["x"], self.e_pos5["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[6], midleft=(self.e_pos6["x"], self.e_pos6["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[7], midleft=(self.e_pos7["x"], self.e_pos7["y"]), **self.text_kwargs)
        utils.ptext.draw(self.e_choices[8], midleft=(self.e_pos8["x"], self.e_pos8["y"]), **self.text_kwargs)

        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == "1":
            pass

        elif self.choices[self.index] == "2":
            pass

        elif self.choices[self.index] == "3":
            pass

        elif self.choices[self.index] == "4":
            pass

    def move_selector(self):
        if self.keybind["up"]:
            self.game.selector_sound.play()
            self.index = (self.index - 1) % len(self.choices)
            self.selector_rect.centery = (self.pos0["y"] + self.selector_offset["y"]) + \
                                         (self.index * self.index_spacing)
        elif self.keybind["down"]:
            self.game.selector_sound.play()
            self.index = (self.index + 1) % len(self.choices)
            self.selector_rect.centery = (self.pos0["y"] + self.selector_offset["y"]) + \
                                         (self.index * self.index_spacing)

        elif self.keybind["left"]:
            pass

        elif self.keybind["right"]:
            pass
