import pygame as pg
from .state import State


class Overworld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        pg.mixer.music.unload()

        self.name = "Overworld"

    def fog(self):
        # TODO: implement overworld fog
        pass

    def update(self):
        self.game.all_sprites.update()
        self.game.camera.update(self.game.player.sprite)

    def render(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply(sprite))
            if sprite.adjustable_layer:
                self.game.all_sprites.change_layer(sprite, sprite.rect.bottom)

        if self.game.draw_debug:
            pg.draw.rect(self.game.screen, (255, 255, 255),
                         self.game.camera.apply_rect(self.game.player.sprite.rect), 1)
            groups = [self.game.npcs, self.game.entity, self.game.cleaner, self.game.obstacles, self.game.closed_doors,
                      self.game.opened_doors, self.game.interactables, self.game.items]
            for group in groups:
                for x in group:
                    pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(x.rect), 1)
