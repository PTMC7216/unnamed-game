import pygame as pg
import json
import random
import src.utils as utils
from .menu import Menu
from .pausewin import PauseWin


class DialogueWin(Menu):
    def __init__(self, game, npc):
        Menu.__init__(self, game)
        self.game = game
        self.npc = npc

        self.framer = utils.Framer(self.game)
        self.typewriter = utils.Typewriter(self.game)

        self.main_frame = self.framer.make_centered_frame(1.2, 3.6)
        self.gap = 20
        self.padding = 15

        self.portrait_win_surf = pg.Surface((self.main_frame.h, self.main_frame.h)).convert()
        self.portrait_win_surf.fill((0, 0, 0))
        self.portrait_win_rect = self.portrait_win_surf.get_rect(
            topleft=(self.main_frame.x, self.main_frame.y))
        self.portrait_pos = (self.portrait_win_rect.x + self.padding,
                             self.portrait_win_rect.y + self.padding)

        self.text_win_surf = pg.Surface((self.main_frame.w - self.main_frame.h - self.gap, self.main_frame.h)).convert()
        self.text_win_surf.fill((0, 0, 0))
        self.text_win_rect = self.text_win_surf.get_rect(
            topleft=(self.main_frame.x + self.main_frame.h + self.gap, self.main_frame.y))
        self.speaker_pos = {"x": self.text_win_rect.x + self.padding,
                            "y": self.text_win_rect.y + self.padding}
        self.text_pos = {"x": self.text_win_rect.x + self.padding,
                         "y": self.text_win_rect.y + self.padding + 40}
        self.choice1_pos = {"x": self.text_win_rect.x + self.padding,
                            "y": self.text_win_rect.y + 120}
        self.choice2_pos = {"x": self.text_win_rect.x + self.padding,
                            "y": self.text_win_rect.y + 140}
        self.choice3_pos = {"x": self.text_win_rect.x + self.padding,
                            "y": self.text_win_rect.y + 160}

        self.text_kwargs = {"width": self.text_win_rect.w - self.padding, "owidth": 1, "ocolor": (0, 0, 0)}
        self.choice_kwargs = {"fontsize": 35, "owidth": 1, "ocolor": (0, 0, 0)}

        self.selector_rect = pg.Rect(0, 0, 20, 20)
        self.selector_offset = {"x": -25, "y": -2}
        self.selector_rect.center = ((self.choice1_pos["x"] + self.selector_offset["x"]),
                                     (self.choice1_pos["y"] + self.selector_offset["y"]))

        self.speaker = None
        self.portrait = None
        self.text = None
        self.text_index = 0
        self.choices = []
        self.choices_index = 0
        self.selecting = False
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.event_link = None
        self.link = None
        self.quiet_link = None

        self.dialogue = None

        self.get_dialogue()

    def refresh_dialogue(self):
        self.text_index = 0
        self.choices = []
        self.choices_index = 0
        self.selecting = False
        self.c1 = None
        self.c2 = None
        self.c3 = None
        self.event_link = None
        self.link = None
        self.quiet_link = None

        self.get_dialogue()

        self.typewriter.reset()

    def set_dialogue(self):
        self.dialogue = self.text[self.text_index]

    def dialogue_base(self):
        self.npc.dialogue_section = "n_0000"
        self.get_dialogue()

    def get_dialogue(self):
        dialogue_file = self.npc.name.lower().replace(" ", "")
        with open(f'./data/dialogues/{dialogue_file}.json', 'r') as f:
            data = json.loads(f.read())

            # INTRO CHECK
            if self.npc.dialogue_section == "check":
                for checker in data[self.npc.dialogue_section]:

                    if "event_item" in checker:
                        if not self.game.player.sprite.inventory:
                            self.dialogue_base()
                        for item in self.game.player.sprite.inventory:
                            if item.name == checker["event_item"]:
                                self.event_link = checker["event_link"]
                                self.npc.dialogue_section = self.event_link
                                self.refresh_dialogue()
                                self.set_dialogue()
                            else:
                                self.dialogue_base()

            else:
                # IDENTITY
                self.speaker = data[self.npc.dialogue_section]['speaker']
                self.portrait = pg.image.load(
                    f"./data/images/portraits/"
                    f"{data[self.npc.dialogue_section]['portrait']}.jpg").convert()
                # TODO: remove image scaling once ui size is decided
                self.portrait = pg.transform.scale(self.portrait,
                                                   (self.portrait_win_rect.w - self.padding * 2,
                                                    self.portrait_win_rect.h - self.padding * 2))

                # TEXT
                if "text" in data[self.npc.dialogue_section]:
                    self.text = data[self.npc.dialogue_section]['text']
                    self.set_dialogue()

                if "text_random" in data[self.npc.dialogue_section]:
                    self.text = data[self.npc.dialogue_section]['text_random'][
                        random.randint(0, len(data[self.npc.dialogue_section]['text_random']) - 1)]
                    self.set_dialogue()

                # CHOICES
                if "choices" in data[self.npc.dialogue_section]:
                    for choice in data[self.npc.dialogue_section]["choices"]:
                        self.choices.append(choice)

                if "choices_conditional" in data[self.npc.dialogue_section]:
                    for condition in data[self.npc.dialogue_section]["choices_conditional"]:

                        if "memory" in condition:
                            if condition["memory"][0] in self.npc.dialogue_memory:
                                for choice in condition["memory"][1:]:
                                    self.choices.append(choice)

                # COMMANDS
                if "commands" in data[self.npc.dialogue_section]:
                    for command in data[self.npc.dialogue_section]["commands"]:

                        if "counter" in command and self.npc.dialogue_counter < (command["counter"] - 1):
                            self.npc.dialogue_counter += 1

                        if "memorize" in command:
                            if command["memorize"] not in self.npc.dialogue_memory:
                                self.npc.dialogue_memory.append(command["memorize"])

                        if "event_item" in command:
                            for item in self.game.player.sprite.inventory:
                                if item.name == command["event_item"]:
                                    self.npc.dialogue_counter = 0
                                    self.npc.dialogue_section = command["event_link"]
                                    self.refresh_dialogue()
                                    self.set_dialogue()

                        if "link" in command:
                            self.npc.dialogue_counter = 0
                            self.link = command["link"]

                        if "quiet_link" in command:
                            self.npc.dialogue_counter = 0
                            self.quiet_link = command["quiet_link"]

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
                self.c1 = list(self.choices[0].values())[0]
                self.c2 = list(self.choices[1].values())[0]
            elif len(self.choices) == 3:
                self.c1 = list(self.choices[0].values())[0]
                self.c2 = list(self.choices[1].values())[0]
                self.c3 = list(self.choices[2].values())[0]

        elif self.text_index == (len(self.text) - 1) and self.link:
            self.npc.dialogue_section = self.link
            self.refresh_dialogue()

        elif self.text_index == (len(self.text) - 1) and self.quiet_link:
            self.npc.dialogue_section = self.quiet_link
            self.movement_key_check()
            self.exit_state()

        else:
            self.movement_key_check()
            self.exit_state()

    def select_choice(self):
        if list(self.choices[self.choices_index].values())[0] == self.c1:
            self.npc.dialogue_section = list(self.choices[self.choices_index])[0]
        elif list(self.choices[self.choices_index].values())[0] == self.c2:
            self.npc.dialogue_section = list(self.choices[self.choices_index])[0]
        elif list(self.choices[self.choices_index].values())[0] == self.c3:
            self.npc.dialogue_section = list(self.choices[self.choices_index])[0]
        self.refresh_dialogue()

    def draw_selector(self):
        if self.selecting:
            utils.ptext.draw(">", self.selector_rect.center, **self.choice_kwargs)

    def move_selector(self):
        if self.choices and self.selecting:
            if self.keybind["up"]:
                self.game.selector_sound.play()
                self.choices_index = (self.choices_index - 1) % len(self.choices)
                self.selector_rect.centery = \
                    (self.choice1_pos["y"] + self.selector_offset["y"]) + (self.choices_index * 20)

            elif self.keybind["down"]:
                self.game.selector_sound.play()
                self.choices_index = (self.choices_index + 1) % len(self.choices)
                self.selector_rect.centery = \
                    (self.choice1_pos["y"] + self.selector_offset["y"]) + (self.choices_index * 20)

    def update(self):
        self.check_events()
        self.move_selector()

        if self.keybind["z"]:
            self.advance_dialogue()
            self.game.select_sound.play()

        elif self.keybind["x"]:
            if not self.selecting:
                self.advance_dialogue()
            self.game.select_sound.play()

        elif self.keybind["esc"]:
            self.game.select_sound.play()
            PauseWin(self.game).enter_state()

        self.key_reset()

    def render(self):
        self.prev_state.render()

        self.game.screen.blit(self.portrait_win_surf, self.portrait_win_rect)
        self.game.screen.blit(self.portrait, self.portrait_pos)

        self.game.screen.blit(self.text_win_surf, self.text_win_rect)

        utils.ptext.draw(self.speaker, (self.speaker_pos["x"], self.speaker_pos["y"]),
                         **self.text_kwargs)

        utils.ptext.draw(self.typewriter.print(self.dialogue), (self.text_pos["x"], self.text_pos["y"]),
                         **self.text_kwargs)

        utils.ptext.draw(self.c1, (self.choice1_pos["x"], self.choice1_pos["y"]), **self.choice_kwargs)
        utils.ptext.draw(self.c2, (self.choice2_pos["x"], self.choice2_pos["y"]), **self.choice_kwargs)
        utils.ptext.draw(self.c3, (self.choice3_pos["x"], self.choice3_pos["y"]), **self.choice_kwargs)

        self.draw_selector()
