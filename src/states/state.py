class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None
        self.prev2_state = None

    def __repr__(self):
        return self.name

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        if len(self.game.state_stack) > 2:
            self.prev2_state = self.game.state_stack[-2]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()

    def exit_states(self, n):
        for i in range(n):
            self.game.state_stack.pop()
