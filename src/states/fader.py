import pygame as pg
from .state import State


class Fader(State):
    def __init__(self, game, state_exits, state_depth, next_state):
        """
        Fades out to next_state. When next_state exits, fades in to a previous state.

        :param game: Game object
        :param state_exits: Exit this many states after fade-in
        :param state_depth: Render at this depth during fade-in
        :param next_state: Transition to this state after fade-out
        """
        super().__init__(game)
        self.state_exits = state_exits
        self.state_depth = state_depth
        self.next_state = next_state

        self.name = 'Fader'

        self.alpha = 0
        self.faded = False
        self.surf = pg.Surface(self.game.camera.rect.size)
        self.surf.fill((0, 0, 0))

        pg.time.set_timer(pg.USEREVENT, 100)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.active = False

            if event.type == pg.USEREVENT:
                if not self.faded:
                    self.alpha += 8
                    if self.alpha >= 255:
                        self.faded = True
                        self.next_state.enter_state()
                else:
                    self.game.state_stack[-self.state_depth].render()
                    self.alpha -= 8
                    if self.alpha <= 0:
                        self.exit_states(self.state_exits)

                self.surf.set_alpha(self.alpha)
                self.game.screen.blit(self.surf, (0, 0))

    def render(self):
        pass
