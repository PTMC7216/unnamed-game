import pygame as pg
import src.utils as utils
from .menu import Menu
from .invcontextwin import InvContextWin


class InventoryWin(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.name = 'Inventory Window'
        self.choices = ["- - -"] * self.game.player.sprite.inventory_size
        for i, item in enumerate(self.game.player.sprite.inventory):
            self.choices[i] = item.name

        self.frame = self.framer.make_center_frame(2, 2)
        self.panel = self.framer.make_panel(self.frame.w, self.frame.h, (10, 10, 10),
                                            topleft=(self.frame.x, self.frame.y))

        self.pos_adj = {'x': self.panel['rect'].w // 2, 'y': self.panel['rect'].h // 4}
        self.title_pos = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'])
        self.pos0 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 50)
        self.pos1 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 90)
        self.pos2 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 130)
        self.pos3 = self.framer.set_pos(self.panel, x=self.pos_adj['x'], y=self.pos_adj['y'] + 170)

        self.c_spacing = 40
        self.position_selector(self.pos0, -90, -2)

        self.text_kwargs = {'owidth': 1, 'ocolor': (0, 0, 0)}

    def refresh(self):
        self.choices = ["- - -"] * 4
        for i, item in enumerate(self.game.player.sprite.inventory):
            self.choices[i] = item.name

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
        self.prev2_state.render()
        self.game.screen.blit(self.panel['surf'], self.panel['rect'])

        utils.ptext.draw('INVENTORY', center=(self.title_pos['x'], self.title_pos['y']))

        utils.ptext.draw(self.choices[0], center=(self.pos0['x'], self.pos0['y']))
        utils.ptext.draw(self.choices[1], center=(self.pos1['x'], self.pos1['y']))
        utils.ptext.draw(self.choices[2], center=(self.pos2['x'], self.pos2['y']))
        utils.ptext.draw(self.choices[3], center=(self.pos3['x'], self.pos3['y']))

        self.draw_selector()

    def transition_state(self):
        selection = self.choices[self.index]
        for item in self.game.player.sprite.inventory:
            if item.name == selection:
                InvContextWin(self.game, item).enter_state()
                break


class TransferWin(InventoryWin):
    # TODO: Open a transferral window for opened chests and traders,
    #  allowing for transferrals between chest/trader and player inventories
    def __init__(self):
        super().__init__(InventoryWin)

        self.name = 'Transfer Window'
