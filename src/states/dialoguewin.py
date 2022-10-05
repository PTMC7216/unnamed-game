import pygame as pg
import json
import random
import src.utils as utils
from .menu import Menu
from .pausewin import PauseWin


class DialogueWin(Menu):
    def __init__(self, game, npc):
        super().__init__(game)
        self.npc = npc

        self.name = 'Dialogue Window'

        self.typewriter = utils.Typewriter(self.game)

        self.frame = self.framer.make_lower_frame(1.2, 3.6)
        self.gap = 20
        self.padding = 15

        self.portrait_panel = \
            self.framer.make_panel(self.frame.h, self.frame.h, (10, 10, 10),
                                   topleft=(self.frame.x, self.frame.y))

        self.portrait_pos = self.framer.set_pos(self.portrait_panel, self.padding)

        self.text_panel = \
            self.framer.make_panel(self.frame.w - self.frame.h - self.gap, self.frame.h, (10, 10, 10),
                                   topleft=(self.frame.x + self.frame.h + self.gap, self.frame.y))

        self.choices_panel = \
            self.framer.make_panel(self.frame.w - self.frame.h - self.gap, self.frame.h / 1.2, (10, 10, 10),
                                   bottomleft=(self.frame.x + self.frame.h + self.gap, self.frame.y - self.gap))

        self.speaker_pos = self.framer.set_pos(self.text_panel, self.padding)
        self.text_pos = self.framer.set_pos(self.text_panel, self.padding, y=40)
        self.pos0 = self.framer.set_pos(self.choices_panel, self.padding, y=0)
        self.pos1 = self.framer.set_pos(self.choices_panel, self.padding, y=30)
        self.pos2 = self.framer.set_pos(self.choices_panel, self.padding, y=60)
        self.pos3 = self.framer.set_pos(self.choices_panel, self.padding, y=90)

        self.position_selector(self.pos0, -11, -2)

        self.choices = []
        self.index_spacing = 30

        self.text_kwargs = {'width': self.text_panel['rect'].w - self.padding}
        self.choice_kwargs = {'width': self.choices_panel['rect'].w - self.padding, 'fontsize': 35}

        self.speaker = None
        self.portrait = None
        self.text = None
        self.text_index = 0
        self.selecting = False
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.event_link = None
        self.link = None
        self.quiet_link = None
        self.giver = False
        self.taker = False
        self.to_give = None
        self.to_take = None
        self.dialogue = None
        self.dialogue_font = None
        self.dialogue_speed = 0

        self.get_dialogue()

    def refresh_dialogue(self):
        self.text_index = 0
        self.choices = []
        self.index = 0
        self.selecting = False
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.event_link = None
        self.link = None
        self.quiet_link = None

        self.get_dialogue()

        self.typewriter.reset()

    def set_dialogue(self):
        self.dialogue = self.text[self.text_index]

    def dialogue_base(self):
        self.npc.dialogue_section = 'n_0000'
        self.get_dialogue()

    def get_dialogue(self):
        dialogue_file = utils.set_path(f"./data/dialogues/{self.npc.name.lower().replace(' ', '')}.json")

        with open(dialogue_file, 'r') as f:
            data = json.loads(f.read())
            priority = []

            # INTRO CHECK
            if self.npc.dialogue_section == 'check':
                for check in data[self.npc.dialogue_section]:

                    if 'event_item' in check:
                        if check['event_item'] in self.game.player.sprite.inventory + self.game.player.sprite.equipment:
                            priority.append(check['event_link'])
                        else:
                            self.dialogue_base()
                            break

                    if 'event_other' in check:
                        if check['event_other'] in self.npc.flags:
                            priority.append(check['event_link'])
                        else:
                            self.dialogue_base()
                            break

                if priority:
                    self.event_link = priority[-1]
                    self.npc.dialogue_section = self.event_link
                    self.refresh_dialogue()
                    self.set_dialogue()

            else:
                # IDENTITY
                if data[self.npc.dialogue_section]['speaker'] == 'Player':
                    self.speaker = self.game.player.sprite.name
                    self.portrait = self.game.player.sprite.portrait
                    self.dialogue_font = self.game.player.sprite.dialogue_font
                    self.dialogue_speed = self.game.player.sprite.dialogue_speed
                else:
                    self.speaker = data[self.npc.dialogue_section]['speaker']
                    self.portrait = self.npc.portrait
                    self.dialogue_font = self.npc.dialogue_font
                    self.dialogue_speed = self.npc.dialogue_speed

                # TEXT
                if 'text' in data[self.npc.dialogue_section]:
                    self.text = data[self.npc.dialogue_section]['text']
                    self.set_dialogue()

                if 'text_random' in data[self.npc.dialogue_section]:
                    self.text = data[self.npc.dialogue_section]['text_random'][
                        random.randint(0, len(data[self.npc.dialogue_section]['text_random']) - 1)]
                    self.set_dialogue()

                # CHOICES
                if 'choices' in data[self.npc.dialogue_section]:
                    for choice in data[self.npc.dialogue_section]['choices']:
                        self.choices.append(choice)

                if 'choices_conditional' in data[self.npc.dialogue_section]:
                    for condition in data[self.npc.dialogue_section]['choices_conditional']:

                        if 'memory' in condition:
                            if condition['memory'][0] in self.npc.dialogue_memory:
                                for choice in condition['memory'][1:]:
                                    self.choices.append(choice)

                # COMMANDS
                if 'commands' in data[self.npc.dialogue_section]:
                    for command in data[self.npc.dialogue_section]['commands']:

                        if 'counter' in command and self.npc.dialogue_counter < (command['counter'] - 1):
                            self.npc.dialogue_counter += 1
                            break

                        if 'memorize' in command:
                            if command['memorize'] not in self.npc.dialogue_memory:
                                self.npc.dialogue_memory.append(command['memorize'])

                        if 'event_item' in command:
                            for item in self.game.player.sprite.inventory + self.game.player.sprite.equipment:
                                if item != 'None' and item.name == command['event_item']:
                                    priority.append(command['event_link'])

                        if 'event_other' in command:
                            if self.npc.flags:
                                for flag in self.npc.flags:
                                    if flag == command['event_other']:
                                        priority.append(command['event_link'])

                        if priority:
                            self.event_link = priority[-1]
                            self.npc.dialogue_counter = 0
                            self.npc.dialogue_section = self.event_link
                            self.refresh_dialogue()
                            self.set_dialogue()

                        if 'link' in command:
                            self.npc.dialogue_counter = 0
                            self.link = command['link']

                        if 'quiet_link' in command:
                            self.npc.dialogue_counter = 0
                            self.quiet_link = command['quiet_link']

                        if 'give' in command:
                            self.npc.dialogue_counter = 0
                            self.giver = True
                            self.to_give = command['give']

                        if 'take' in command:
                            self.npc.dialogue_counter = 0
                            self.taker = True
                            self.to_take = command['take']

                        if 'set_step' in command:
                            self.npc.dialogue_counter = 0
                            self.npc.step = command['set_step']

    def advance_dialogue(self):
        # if still typewriting, instantly display full text block
        if self.typewriter.i < len(self.typewriter.text_block):
            self.typewriter.i = len(self.typewriter.text_block)

        # progress to the dialogue object's next text list value
        elif self.text_index < (len(self.text) - 1):
            self.text_index += 1
            self.typewriter.reset()
            self.dialogue = self.text[self.text_index]

        elif self.selecting:
            self.select_choice()

        elif self.text_index == (len(self.text) - 1) and self.choices:
            self.selecting = True
            if len(self.choices) == 1:
                self.c1 = list(self.choices[0].values())[0]
            elif len(self.choices) == 2:
                self.c1, self.c2 = [list(self.choices[i].values())[0] for i in range(2)]
            elif len(self.choices) == 3:
                self.c1, self.c2, self.c3 = [list(self.choices[i].values())[0] for i in range(3)]
            elif len(self.choices) == 4:
                self.c1, self.c2, self.c3, self.c4 = [list(self.choices[i].values())[0] for i in range(4)]

        elif self.text_index == (len(self.text) - 1) and self.link:
            self.npc.dialogue_section = self.link
            self.refresh_dialogue()

        elif self.text_index == (len(self.text) - 1) and self.quiet_link:
            self.npc.dialogue_section = self.quiet_link
            self.game.player.sprite.movement_key_check()
            self.exit_state()
            self.transferrals()

        else:
            self.game.player.sprite.movement_key_check()
            self.exit_state()
            self.transferrals()

    def transferrals(self):
        if self.giver:
            self.npc.give_item(self.to_give)
        elif self.taker:
            self.npc.take_item(self.to_take)

    def select_choice(self):
        self.npc.dialogue_section = list(self.choices[self.index])[0]
        self.position_selector(self.pos0, -11, -2)
        self.refresh_dialogue()

    def draw_selector(self):
        if self.selecting:
            utils.ptext.draw('>', self.selector_rect.center, **self.choice_kwargs)

    def move_selector(self):
        if self.choices and self.selecting:
            if self.keybool['up']:
                self.game.selector_sound.play()
                self.index = (self.index - 1) % len(self.choices)
                self.selector_rect.centery = (self.pos0['y'] + self.selector_offset['y']) + \
                                             (self.index * self.index_spacing)

            elif self.keybool['down']:
                self.game.selector_sound.play()
                self.index = (self.index + 1) % len(self.choices)
                self.selector_rect.centery = (self.pos0['y'] + self.selector_offset['y']) + \
                                             (self.index * self.index_spacing)

    def update(self):
        self.check_events()
        self.move_selector()
        if self.keybool['z']:
            self.advance_dialogue()
            self.game.select_sound.play()
        elif self.keybool['x']:
            if not self.selecting:
                self.advance_dialogue()
            self.game.select_sound.play()
        elif self.keybool['esc']:
            self.game.select_sound.play()
            self.exit_state()
        self.key_reset()

    def render(self):
        self.prev_state.render()

        self.game.screen.blit(self.portrait_panel['surf'], self.portrait_panel['rect'])
        self.game.screen.blit(self.portrait, (self.portrait_pos['x'], self.portrait_pos['y']))

        self.game.screen.blit(self.text_panel['surf'], self.text_panel['rect'])
        utils.ptext.draw(self.speaker, (self.speaker_pos['x'], self.speaker_pos['y']), **self.text_kwargs)
        utils.ptext.draw(self.typewriter.print(self.dialogue, self.dialogue_speed),
                         (self.text_pos['x'], self.text_pos['y']), fontname=self.dialogue_font,
                         **self.text_kwargs)

        if self.selecting:
            self.game.screen.blit(self.choices_panel['surf'], self.choices_panel['rect'])
            utils.ptext.draw(self.c1, (self.pos0['x'], self.pos0['y']), **self.choice_kwargs)
            utils.ptext.draw(self.c2, (self.pos1['x'], self.pos1['y']), **self.choice_kwargs)
            utils.ptext.draw(self.c3, (self.pos2['x'], self.pos2['y']), **self.choice_kwargs)
            utils.ptext.draw(self.c4, (self.pos3['x'], self.pos3['y']), **self.choice_kwargs)

        self.draw_selector()
