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
            for npc in self.game.npcs:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(npc.rect), 1)
            for entity in self.game.entity:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(entity.rect), 1)
            for cleaner in self.game.cleaner:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(cleaner.rect), 1)
            for obstacle in self.game.obstacles:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(obstacle.rect), 1)
            for closed_door in self.game.closed_doors:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(closed_door.rect), 1)
            for open_door in self.game.opened_doors:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(open_door.rect), 1)
            for interactable in self.game.interactables:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(interactable.rect), 1)
            for item in self.game.items:
                pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(item.rect), 1)
