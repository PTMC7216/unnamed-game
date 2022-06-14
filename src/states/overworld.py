import pygame as pg
import math
from .state import State


class Overworld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        pg.mixer.music.unload()

        self.name = "Overworld"

        self.rays = 40
        self.radius = 300

        self.fog = pg.Surface((self.game.map_rect.w, self.game.map_rect.h)).convert()
        self.fog.fill((0, 0, 0))
        self.fog.set_colorkey((1, 1, 1))

    def main_blit(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply(sprite))
            if sprite.adjustable_layer:
                self.game.all_sprites.change_layer(sprite, sprite.rect.bottom)

    def fog_blit(self):
        self.game.screen.blit(self.fog, self.game.camera.apply_rect(self.game.map_rect))

    # TODO: overworld explored blit
    def explored_blit(self):
        pass

    # TODO: overworld sight blit
    def sight_blit(self):
        rects = []
        for obstacle in self.game.obstacles:
            rects.append(self.game.camera.apply_rect(obstacle.rect))
        for door in self.game.closed_doors:
            rects.append(self.game.camera.apply_rect(door.rect))

        src_pos = (self.game.camera.apply_rect(self.game.player.sprite.rect).centerx,
                   self.game.camera.apply_rect(self.game.player.sprite.rect).centery)

        for i in range(self.rays):
            fin_pos = (self.radius * math.cos(2 * math.pi / self.rays * i) + src_pos[0],
                       self.radius * math.sin(2 * math.pi / self.rays * i) + src_pos[1])

            for rect in rects:
                for vert_1, vert_2 in [(rect.bottomright, rect.topright), (rect.topright, rect.topleft),
                                       (rect.topleft, rect.bottomleft), (rect.bottomleft, rect.bottomright)]:
                    d = (src_pos[0] - fin_pos[0]) * (vert_1[1] - vert_2[1]) - \
                           (src_pos[1] - fin_pos[1]) * (vert_1[0] - vert_2[0])
                    if d != 0:
                        n_1 = ((vert_2[0] - src_pos[0]) * (src_pos[1] - fin_pos[1]) -
                               (vert_2[1] - src_pos[1]) * (src_pos[0] - fin_pos[0])) / d
                        n_2 = ((vert_2[0] - src_pos[0]) * (vert_2[1] - vert_1[1]) -
                               (vert_2[1] - src_pos[1]) * (vert_2[0] - vert_1[0])) / d
                        if 0 <= n_1 <= 1 and 0 <= n_2 <= 1:
                            p_x = src_pos[0] + n_2 * (fin_pos[0] - src_pos[0])
                            p_y = src_pos[1] + n_2 * (fin_pos[1] - src_pos[1])
                            fin_pos = (p_x, p_y)

            pg.draw.line(self.game.screen, 'white', src_pos, fin_pos)
            # TODO: Implement Bresenham's line algorithm
            # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

    def reveal_location(self, x, y, size):
        pg.draw.circle(self.fog, (1, 1, 1), (x, y), size)

    def update(self):
        self.game.all_sprites.update()
        self.game.camera.update(self.game.player.sprite)

    def render(self):
        self.main_blit()
        self.fog_blit()
        self.sight_blit()

        if self.game.draw_debug:
            pg.draw.rect(self.game.screen, (255, 255, 255),
                         self.game.camera.apply_rect(self.game.player.sprite.rect), 1)
            groups = [self.game.npcs, self.game.entity, self.game.cleaner, self.game.obstacles, self.game.closed_doors,
                      self.game.opened_doors, self.game.interactables, self.game.items]
            for group in groups:
                for x in group:
                    pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(x.rect), 1)
