import pygame as pg
import math
from .state import State


class Overworld(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.name = 'Overworld'

        self.rays = 60
        self.radius = self.game.player.sprite.radius
        self.src_pos = None
        self.fin_pos = None

    def line_of_sight(self):
        self.src_pos = self.game.player.sprite.rect.center

        obstacle_list = pg.sprite.spritecollide(self.game.player.sprite, self.game.obstacles,
                                                False, pg.sprite.collide_circle_ratio(1.0))

        door_list = pg.sprite.spritecollide(self.game.player.sprite, self.game.closed_doors,
                                            False, pg.sprite.collide_circle_ratio(1.0))

        fog_list = pg.sprite.spritecollide(self.game.player.sprite, self.game.fog,
                                           False, pg.sprite.collide_circle_ratio(1.0))

        for i in range(self.rays):
            self.fin_pos = (self.radius * math.cos(2 * math.pi / self.rays * i) + self.src_pos[0],
                            self.radius * math.sin(2 * math.pi / self.rays * i) + self.src_pos[1])

            a = pg.math.Vector2(self.src_pos)
            b = pg.math.Vector2(self.fin_pos)
            angle = pg.math.Vector2().angle_to(a - b)

            for sprite in obstacle_list + door_list:
                if -0 >= angle >= -180:
                    self.ray_collision((sprite.rect.topleft, sprite.rect.topright), 0, 2)
                if 0 <= angle <= 180:
                    self.ray_collision((sprite.rect.bottomright, sprite.rect.bottomleft), 0, -2)

                self.ray_collision((sprite.rect.topright, sprite.rect.bottomright), -2, 0)

                self.ray_collision((sprite.rect.bottomleft, sprite.rect.topleft), 2, 0)

            for fog in fog_list:
                if fog.rect.clipline(self.src_pos, self.fin_pos):
                    fog.in_los()

    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    def ray_collision(self, rect_edge: tuple, xmod: int, ymod: int):
        for vert_1, vert_2 in [rect_edge]:
            d = (self.src_pos[0] - self.fin_pos[0]) * (vert_1[1] - vert_2[1]) - \
                (self.src_pos[1] - self.fin_pos[1]) * (vert_1[0] - vert_2[0])
            if d != 0:
                n_1 = ((vert_2[0] - self.src_pos[0]) * (self.src_pos[1] - self.fin_pos[1]) -
                       (vert_2[1] - self.src_pos[1]) * (self.src_pos[0] - self.fin_pos[0])) / d
                n_2 = ((vert_2[0] - self.src_pos[0]) * (vert_2[1] - vert_1[1]) -
                       (vert_2[1] - self.src_pos[1]) * (vert_2[0] - vert_1[0])) / d
                if 0 <= n_1 <= 1 and 0 <= n_2 <= 1:
                    p_x = self.src_pos[0] + n_2 * (self.fin_pos[0] - self.src_pos[0])
                    p_y = self.src_pos[1] + n_2 * (self.fin_pos[1] - self.src_pos[1])
                    self.fin_pos = (p_x + xmod, p_y + ymod)

    def update(self):
        self.game.all_sprites.update()
        self.game.camera.update(self.game.player.sprite)

    def render(self):
        # self.line_of_sight()

        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply_sprite(sprite))
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
