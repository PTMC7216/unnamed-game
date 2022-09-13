import pygame as pg
import src.utils as utils
from src.states.menu import Menu


class StatusWin(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.name = "Status Window"

        self.frame = self.framer.make_center_frame(2, 1.93)
        self.gap = 10
        self.padding = 10

        self.c_panel = self.framer.make_panel((self.frame.w // 3) - self.gap, self.frame.h - 150,
                                              bottomleft=(self.frame.x + self.gap, (self.frame.y * 2) - self.gap),
                                              color=(100, 100, 100))

        self.c_adj = {'x': self.padding, 'y': self.padding - 2}
        self.c_name_pos = self.framer.set_pos(self.c_panel, x=self.c_adj['x'], y=self.c_adj['y'])
        self.c_title_pos = self.framer.set_pos(self.c_panel, x=self.c_adj['x'], y=self.c_adj['y'] + 30)
        self.c_lv_pos = self.framer.set_pos(self.c_panel, x=self.c_adj['x'], y=self.c_adj['y'] + 60)
        self.c_hp_pos = self.framer.set_pos(self.c_panel, x=self.c_adj['x'], y=self.c_adj['y'] + 90)
        self.c_mp_pos = self.framer.set_pos(self.c_panel, x=self.c_adj['x'], y=self.c_adj['y'] + 120)

        self.s_panel = self.framer.make_panel((self.frame.w // 3) - self.gap, self.frame.h - 120,
                                              topleft=(self.frame.x + self.gap, self.frame.y * 2),
                                              color=(100, 100, 100))

        self.s_adj = {'x': self.padding, 'y': self.padding + 10}
        self.pos0 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'])
        self.pos1 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'] + 30)
        self.pos2 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'] + 60)
        self.pos3 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'] + 90)
        self.pos4 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'] + 120)
        self.pos5 = self.framer.set_pos(self.s_panel, x=self.s_adj['x'], y=self.s_adj['y'] + 150)

        self.e_panel = self.framer.make_panel((self.frame.w // 1.5) - self.gap, self.frame.h + 50,
                                              topleft=((self.frame.w // 1.2) + self.gap, self.frame.y - 25),
                                              color=(100, 100, 100))

        self.e_adj = {'x': self.padding, 'y': self.padding + 10}
        self.e_pos0 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'])
        self.e_pos1 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 30)
        self.e_pos2 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 60)
        self.e_pos3 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 90)
        self.e_pos4 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 120)
        self.e_pos5 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 150)
        self.e_pos6 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 180)
        self.e_pos7 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 210)
        self.e_pos8 = self.framer.set_pos(self.e_panel, x=self.e_adj['x'], y=self.e_adj['y'] + 240)

        self.col1 = {'choices': ['STR', 'DEX', 'AGI', 'INT', 'CHA'],
                     'pos': self.pos0}
        self.col2 = {'choices': ['R Hand', 'L Hand',
                                 'Accessory 1', 'Accessory 2',
                                 'Head', 'Torso', 'Hands', 'Legs', 'Feet'],
                     'pos': self.e_pos0}
        self.cols = [self.col1, self.col2]
        self.col = 0

        self.choices = self.cols[self.col]
        self.index_spacing = 30

        self.c_spacing = 30
        self.position_selector(self.col1['pos'], -15, -2)

        self.text_kwargs = {'fontsize': 35}

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybool['x']:
            self.game.select_sound.play()
            self.game.player.sprite.movement_key_check()
            self.exit_states(2)
        elif self.keybool['esc']:
            self.game.select_sound.play()
            self.game.player.sprite.movement_key_check()
            self.exit_states(2)
        self.key_reset()

    def render(self):
        self.prev_state.render()
        self.game.screen.blit(self.c_panel['surf'], self.c_panel['rect'])
        self.game.screen.blit(self.s_panel['surf'], self.s_panel['rect'])
        self.game.screen.blit(self.e_panel['surf'], self.e_panel['rect'])

        utils.ptext.draw(self.game.player.sprite.name,
                         topleft=(self.c_name_pos['x'], self.c_name_pos['y']), **self.text_kwargs)
        utils.ptext.draw(self.game.player.sprite.title,
                         topleft=(self.c_title_pos['x'], self.c_title_pos['y']), **self.text_kwargs)
        utils.ptext.draw(f"LV: {self.game.player.sprite.lv}",
                         topleft=(self.c_lv_pos['x'], self.c_lv_pos['y']), **self.text_kwargs)
        utils.ptext.draw(f"HP: {self.game.player.sprite.hp}",
                         topleft=(self.c_hp_pos['x'], self.c_hp_pos['y']), **self.text_kwargs)
        utils.ptext.draw(f"MP: {self.game.player.sprite.mp}",
                         topleft=(self.c_mp_pos['x'], self.c_mp_pos['y']), **self.text_kwargs)

        utils.ptext.draw(f"STR: {self.game.player.sprite.strength}",
                         midleft=(self.pos0['x'], self.pos0['y']), **self.text_kwargs)
        utils.ptext.draw(f"DEX: {self.game.player.sprite.dexterity}",
                         midleft=(self.pos1['x'], self.pos1['y']), **self.text_kwargs)
        utils.ptext.draw(f"AGI: {self.game.player.sprite.agility}",
                         midleft=(self.pos2['x'], self.pos2['y']), **self.text_kwargs)
        utils.ptext.draw(f"INT: {self.game.player.sprite.intelligence}",
                         midleft=(self.pos3['x'], self.pos3['y']), **self.text_kwargs)
        utils.ptext.draw(f"CHA: {self.game.player.sprite.charisma}",
                         midleft=(self.pos4['x'], self.pos4['y']), **self.text_kwargs)
        utils.ptext.draw(f"Unallocated: {self.game.player.sprite.unallocated}",
                         midleft=(self.pos5['x'], self.pos5['y']), fontsize=20)

        utils.ptext.draw(f"R Hand: {self.game.player.sprite.hand[0]}",
                         midleft=(self.e_pos0['x'], self.e_pos0['y']), **self.text_kwargs)
        utils.ptext.draw(f"L Hand: {self.game.player.sprite.hand[1]}",
                         midleft=(self.e_pos1['x'], self.e_pos1['y']), **self.text_kwargs)
        utils.ptext.draw(f"Accessory 1: {self.game.player.sprite.accessory[0]}",
                         midleft=(self.e_pos2['x'], self.e_pos2['y']), **self.text_kwargs)
        utils.ptext.draw(f"Accessory 2: {self.game.player.sprite.accessory[1]}",
                         midleft=(self.e_pos3['x'], self.e_pos3['y']), **self.text_kwargs)
        utils.ptext.draw(f"Head: {self.game.player.sprite.head}",
                         midleft=(self.e_pos4['x'], self.e_pos4['y']), **self.text_kwargs)
        utils.ptext.draw(f"Torso: {self.game.player.sprite.torso}",
                         midleft=(self.e_pos5['x'], self.e_pos5['y']), **self.text_kwargs)
        utils.ptext.draw(f"Hands: {self.game.player.sprite.hands}",
                         midleft=(self.e_pos6['x'], self.e_pos6['y']), **self.text_kwargs)
        utils.ptext.draw(f"Legs: {self.game.player.sprite.legs}",
                         midleft=(self.e_pos7['x'], self.e_pos7['y']), **self.text_kwargs)
        utils.ptext.draw(f"Feet: {self.game.player.sprite.feet}",
                         midleft=(self.e_pos8['x'], self.e_pos8['y']), **self.text_kwargs)

        self.draw_selector()

    def transition_state(self):
        if self.choices['choices'][self.index] == '1':
            pass

        elif self.choices['choices'][self.index] == '2':
            pass

        elif self.choices['choices'][self.index] == '3':
            pass

        elif self.choices['choices'][self.index] == '4':
            pass

    def row_move(self, direction):
        """Pass an "up" or "down" argument to move the selector in that direction by 1 row."""
        if direction == 'up':
            direction = -1
        else:
            direction = 1
        self.game.selector_sound.play()
        self.index = (self.index + direction) % len(self.choices['choices'])
        self.selector_rect.centery = (self.choices['pos'].get('y') + self.selector_offset['y']) + \
                                     (self.index * self.index_spacing)

    def col_move(self, direction):
        """Pass a "left" or "right" argument to move the selector in that direction by 1 column."""
        if direction == 'left':
            direction = -1
        else:
            direction = 1
        self.game.selector_sound.play()
        self.index = 0
        self.col = (self.col + direction) % len(self.cols)
        self.choices = self.cols[self.col]
        self.position_selector(self.choices['pos'], -15, -2)

    def move_selector(self):
        if self.keybool['up']:
            self.row_move('up')

        elif self.keybool['down']:
            self.row_move('down')

        elif self.keybool['left']:
            self.col_move('left')

        elif self.keybool['right']:
            self.col_move('right')
