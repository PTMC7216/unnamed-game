import pygame as pg
import operator
import src.utils as utils
from .menu import Menu
from .overworld import Overworld


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.name = 'Main Menu'
        self.choices = ['Start', 'Options', 'Quit']

        self.frame = self.framer.make_center_frame()
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, topleft=(self.frame.x, self.frame.y))

        self.pos_adj = {'x': self.panel['rect'].w // 2, 'y': self.panel['rect'].h // 2}
        self.title_pos = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] - 40)
        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 50)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 90)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 130)

        self.c_spacing = 40
        self.position_selector(self.pos0, -90, -2)

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])
        utils.ptext.draw('Main Menu', center=(self.title_pos['x'], self.title_pos['y']))
        utils.ptext.draw(self.choices[0], center=(self.pos0['x'], self.pos0['y']))
        utils.ptext.draw(self.choices[1], center=(self.pos1['x'], self.pos1['y']))
        utils.ptext.draw(self.choices[2], center=(self.pos2['x'], self.pos2['y']))
        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == 'Start':
            self.movement_key_check()
            Overworld(self.game).enter_state()

        elif self.choices[self.index] == 'Options':
            OptionsMenu(self.game).enter_state()

        elif self.choices[self.index] == 'Quit':
            self.game.active = False


class OptionsMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.name = 'Options Menu'
        self.choices = ['Audio', 'Keybinds']
        self.index = 0

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybool['x']:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])
        utils.ptext.draw('Options', center=(self.title_pos['x'], self.title_pos['y']))
        utils.ptext.draw(self.choices[0], center=(self.pos0['x'], self.pos0['y']))
        utils.ptext.draw(self.choices[1], center=(self.pos1['x'], self.pos1['y']))
        self.draw_selector()

    def transition_state(self):
        if self.choices[self.index] == 'Audio':
            AudioMenu(self.game).enter_state()
        elif self.choices[self.index] == 'Keybinds':
            KeybindsMenu(self.game).enter_state()


class AudioMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.name = 'Audio Menu'
        self.choices = ['SFX', 'BGM']
        self.index = 0

    def adjust_volume(self, addsub):
        def adjust(x): return round(addsub(x, 0.1), 1)
        if self.choices[self.index] == 'SFX':
            self.game.selector_sound.set_volume(adjust(self.game.selector_sound.get_volume()))
            self.game.select_sound.set_volume(adjust(self.game.selector_sound.get_volume()))
        elif self.choices[self.index] == 'BGM':
            pg.mixer.music.set_volume(adjust(pg.mixer.music.get_volume()))

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybool['x']:
            self.game.select_sound.play()
            self.exit_state()
        elif self.keybool['left']:
            self.game.select_sound.play()
            self.adjust_volume(operator.sub)
        elif self.keybool['right']:
            self.game.select_sound.play()
            self.adjust_volume(operator.add)
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])
        utils.ptext.draw('Audio', center=(self.title_pos['x'], self.title_pos['y']))

        utils.ptext.draw(self.choices[0], center=(self.pos0['x'] - 30, self.pos0['y']))
        utils.ptext.draw(f'{round(self.game.selector_sound.get_volume(), 1)}',
                         center=(self.pos0['x'] + 30, self.pos0['y']))

        utils.ptext.draw(self.choices[1], center=(self.pos1['x'] - 30, self.pos1['y']))
        utils.ptext.draw(f'{round(pg.mixer.music.get_volume(), 1)}',
                         center=(self.pos1['x'] + 30, self.pos1['y']))
        self.draw_selector()

    def transition_state(self):
        pass


class KeybindsMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.name = 'Keybinds Menu'
        self.choices = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SELECT', 'BACK', 'MOD']
        self.index = 0

        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 20)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 60)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 100)
        self.pos3 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 140)
        self.pos4 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 180)
        self.pos5 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 220)
        self.pos6 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 260)

        self.position_selector(self.pos0, -110, -2)

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.game.select_sound.play()
            self.transition_state()
        elif self.keybool['x']:
            self.game.select_sound.play()
            self.exit_state()
        elif self.keybool['esc']:
            self.game.control = {
                'up': pg.K_UP,
                'down': pg.K_DOWN,
                'left': pg.K_LEFT,
                'right': pg.K_RIGHT,
                'select': pg.K_z,
                'back': pg.K_x,
                'mod': pg.K_LSHIFT
            }
        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])
        utils.ptext.draw('Keybinds \nESC to restore defaults', center=(self.title_pos['x'], self.title_pos['y']))

        utils.ptext.draw(self.choices[0], midleft=(self.pos0['x'] - 90, self.pos0['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['up'])}", midleft=(self.pos0['x'] + 40, self.pos0['y']))

        utils.ptext.draw(self.choices[1], midleft=(self.pos1['x'] - 90, self.pos1['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['down'])}", midleft=(self.pos1['x'] + 40, self.pos1['y']))

        utils.ptext.draw(self.choices[2], midleft=(self.pos2['x'] - 90, self.pos2['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['left'])}", midleft=(self.pos2['x'] + 40, self.pos2['y']))

        utils.ptext.draw(self.choices[3], midleft=(self.pos3['x'] - 90, self.pos3['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['right'])}", midleft=(self.pos3['x'] + 40, self.pos3['y']))

        utils.ptext.draw(self.choices[4], midleft=(self.pos4['x'] - 90, self.pos4['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['select'])}", midleft=(self.pos4['x'] + 40, self.pos4['y']))

        utils.ptext.draw(self.choices[5], midleft=(self.pos5['x'] - 90, self.pos5['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['back'])}", midleft=(self.pos5['x'] + 40, self.pos5['y']))

        utils.ptext.draw(self.choices[6], midleft=(self.pos6['x'] - 90, self.pos6['y']))
        utils.ptext.draw(f"{pg.key.name(self.game.control['mod'])}", midleft=(self.pos6['x'] + 40, self.pos6['y']))
        self.draw_selector()

    def transition_state(self):
        Keybinder(self.game, self.choices[self.index]).enter_state()


class Keybinder(KeybindsMenu):
    def __init__(self, game, bind):
        super().__init__(game)
        self.bind = bind
        self.name = 'Keybinder'

    def update(self):
        self.check_events()

        if self.keybool['esc']:
            self.exit_state()

        elif self.keydown is not None:
            for key, value in self.game.control.items():
                try:
                    if value == pg.key.key_code(self.keydown):
                        self.game.control[key] = self.game.control[self.bind.lower()]
                except ValueError:
                    return

            self.game.control[self.bind.lower()] = pg.key.key_code(self.keydown)
            self.exit_state()

        self.key_reset()

    def render(self):
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])
        utils.ptext.draw(f"Press any key to bind it to {self.bind}", center=(self.title_pos['x'], self.title_pos['y']))
        utils.ptext.draw('ESC to cancel', center=(self.title_pos['x'], self.title_pos['y'] + 40))

    def transition_state(self):
        pass
