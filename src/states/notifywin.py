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
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, (10, 10, 10),
                                            topleft=(self.frame.x, self.frame.y))

        self.notification_pos = self.framer.set_pos(self.panel, self.pad)

        self.text_kwargs = {"width": self.panel["rect"].w - self.pad}

    def update(self):
        self.check_events()

        if self.keybind["z"] or self.keybind["x"]:
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
    def __init__(self, game, obj, c1, c2, step, state_exits, *notices):
        super().__init__(game, state_exits, *notices)

        self.obj = obj
        self.c1 = c1
        self.c2 = c2
        self.step = step

        self.c_pos = self.framer.set_pos(self.panel, self.pad, y=80)
        self.c_index = 0
        self.c_spacing = 30

        self.position_selector(self.c_pos, -14, -2)

        self.selecting = False
        self.choice = self.c1
        self.flag = None

    def update(self):
        self.check_events()

        if self.notice >= len(self.notices) - 1:
            self.selecting = True

        if self.selecting:
            if self.keybind["up"] or self.keybind["down"]:
                self.game.selector_sound.play()
                if self.choice == self.c1:
                    self.choice = self.c2
                    self.c_index = 1
                else:
                    self.choice = self.c1
                    self.c_index = 0
                self.selector_rect.centery = (self.c_pos["y"] + self.selector_offset["y"]) + \
                                             (self.c_index * self.c_spacing)

        if self.keybind["z"]:
            if len(self.notices) > 0 and self.notice < len(self.notices) - 1:
                self.game.select_sound.play()
                self.notice += 1
            else:
                if self.c_index == 0:
                    self.flag = self.c1
                elif self.c_index == 1:
                    self.flag = self.c2
                self.flag_handler()

        if self.keybind["x"]:
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

        if self.selecting:
            utils.ptext.draw(self.c1, (self.c_pos["x"], self.c_pos["y"]), **self.text_kwargs)
            utils.ptext.draw(self.c2, (self.c_pos["x"], self.c_pos["y"] + 30), **self.text_kwargs)
            utils.ptext.draw(">", self.selector_rect.center)

    def flag_handler(self):
        if self.obj == "Pause Window":

            if self.flag == "Yes":
                self.game.select_sound.play()
                pg.mixer.music.load('./data/music/ominous1.ogg')
                pg.mixer.music.play(-1, 0.0, 10000)
                while len(self.game.state_stack) > 1:
                    self.game.state_stack.pop()

            elif self.flag == "No":
                self.game.select_sound.play()
                self.movement_key_check()
                self.exit_states(self.state_exits)

        elif self.obj == "Crystal Switch":

            if self.flag == "Do nothing":
                self.game.select_sound.play()
                self.movement_key_check()
                self.exit_states(self.state_exits)

            elif self.flag == "Touch it":
                self.game.select_sound.play()
                interactable = pg.sprite.spritecollide(self.game.player.sprite, self.game.interactables, False)[-1]
                if interactable.event:
                    interactable.set_flag(interactable.flagged_npc, interactable.flagged_desc)

                door_names = {"Energy Door", "Energy Gate"}
                for door in self.game.closed_doors:
                    if door.name in door_names and door.shield_type == interactable.crystal_type:
                        door.shielded = False
                        door.open()
                        interactable.active = False
                        interactable.image = interactable.inert_img
                        break

                self.movement_key_check()
                NotifyWin(self.game, 2, "The energy within the crystal fades away.").enter_state()

        elif self.obj == "Tele Portal":

            if self.flag == "Do nothing":
                self.game.select_sound.play()
                self.movement_key_check()
                self.exit_states(self.state_exits)

            elif self.flag == "Reach in":
                self.game.select_sound.play()
                touched = pg.sprite.spritecollide(self.game.player.sprite, self.game.interactables, False)[-1]
                if touched.target is None:
                    self.movement_key_check()
                    NotifyWin(self.game, 2, "You are pushed away from the swirling mass.").enter_state()
                else:
                    for interactable in self.game.interactables:
                        if interactable.category == "portal" and interactable.identifier == touched.target:
                            self.game.player.sprite.rect.center = interactable.rect.center
                            break
                    self.movement_key_check()
                    NotifyWin(self.game, 2, "You are pulled into the swirling mass. . .").enter_state()
