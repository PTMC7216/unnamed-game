import pygame as pg
import src.utils as utils
from .menu import Menu
from .notifywin import NotifyWin


class InvContextWin(Menu):
    def __init__(self, game, item):
        super().__init__(game)
        self.item = item

        self.name = 'Inventory Context Window'
        self.choices = ['Use', 'Equip', 'Examine', 'Drop']

        self.frame = self.framer.make_center_frame(4, 2)
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, (10, 10, 10),
                                            topleft=(self.frame.x, self.frame.y))

        self.pos_adj = {'x': self.panel['rect'].w // 2, 'y': self.panel['rect'].h // 4}
        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 50)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 75)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 100)
        self.pos3 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 125)

        self.c_spacing = 25
        self.position_selector(self.pos0, -60, -2)

        if self.item.equipped:
            self.choices[1] = 'Unequip'

        self.text_kwargs = {'fontsize': 32}

    @staticmethod
    def _restriction(restriction_check):
        if restriction_check:
            return 255, 255, 255
        else:
            return 50, 50, 50

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybool['x']:
            self.game.select_sound.play()
            self.game.player.sprite.movement_key_check()
            self.exit_state()
        elif self.keybool['esc']:
            self.game.select_sound.play()
            self.game.player.sprite.movement_key_check()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.prev_state.render()
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])

        utils.ptext.draw(self.choices[0], color=self._restriction(self.item.usable),
                         center=(self.pos0['x'], self.pos0['y']), **self.text_kwargs)

        utils.ptext.draw(self.choices[1], color=self._restriction(self.item.equipable),
                         center=(self.pos1['x'], self.pos1['y']), **self.text_kwargs)

        utils.ptext.draw(self.choices[2], center=(self.pos2['x'], self.pos2['y']), **self.text_kwargs)

        utils.ptext.draw(self.choices[3], color=self._restriction(self.item.droppable),
                         center=(self.pos3['x'], self.pos3['y']), **self.text_kwargs)

        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == 'Use':
            self.item.use()

        elif self.choices[self.index] == 'Equip':
            if not self.item.equipable:
                NotifyWin(self.game, 1, f"Can't equip the {self.item.name}.").enter_state()
            else:
                self.choices[1] = 'Unequip'
                self.item.equip()

        elif self.choices[self.index] == 'Unequip':
            if not self.item.equipped:
                NotifyWin(self.game, 1, f"The {self.item.name} is already unequipped.").enter_state()
            else:
                self.choices[1] = 'Equip'
                self.item.unequip()

        elif self.choices[self.index] == 'Examine':
            self.item.examine()

        elif self.choices[self.index] == 'Drop':
            if not self.item.droppable:
                NotifyWin(self.game, 1, f"Can't drop the {self.item.name}.").enter_state()
            else:
                self.item.drop()
