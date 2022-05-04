class Typewriter:
    def __init__(self, game):
        self.game = game
        self.text = ''
        self.text_block = ''
        self.text_iterator = iter(self.text_block)
        self.i = 0

    def reset(self):
        self.i = 0

    def print(self, string, speed=60):
        self.text_block = string
        self.text_iterator = iter(self.text_block)
        if len(self.text) < len(self.text_block):
            self.text += next(self.text_iterator)
        self.i += speed * self.game.dt
        return self.text_block[:int(self.i)]
