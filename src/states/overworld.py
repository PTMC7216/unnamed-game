import pygame as pg
import math
from .state import State


class Overworld(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        pg.mixer.music.unload()

        self.name = "Overworld"

        self.rays = 120
        self.radius = 300
        self.src_pos = None
        self.fin_pos = None

    def line_of_sight(self):
        rects = [obstacle.rect for obstacle in self.game.obstacles] + \
                [door.rect for door in self.game.closed_doors]

        self.src_pos = (self.game.player.sprite.rect.centerx,
                        self.game.player.sprite.rect.centery)

        for i in range(self.rays):
            self.fin_pos = (self.radius * math.cos(2 * math.pi / self.rays * i) + self.src_pos[0],
                            self.radius * math.sin(2 * math.pi / self.rays * i) + self.src_pos[1])

            for rect in rects:
                self.ray_collision((rect.topleft, rect.topright), 0, 4)
                self.ray_collision((rect.topright, rect.bottomright), -4, 0)
                self.ray_collision((rect.bottomright, rect.bottomleft), 0, -4)
                self.ray_collision((rect.bottomleft, rect.topleft), 4, 0)

            # pg.draw.line(self.game.screen, 'white', self.src_pos, self.fin_pos)
            for fog in self.game.fog.sprites():
                clipped_line = fog.rect.clipline(self.src_pos, self.fin_pos)
                if clipped_line:
                    fog.kill()

            # self.bresenham_plot(*self.src_pos, *self.fin_pos)

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

    # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    def bresenham_plot(self, x0, y0, x1, y1):
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                self.bresenham_plot_low(x1, y1, x0, y0)
            else:
                self.bresenham_plot_low(x0, y0, x1, y1)
        else:
            if y0 > y1:
                self.bresenham_plot_high(x1, y1, x0, y0)
            else:
                self.bresenham_plot_high(x0, y0, x1, y1)

    # noinspection PyMethodMayBeStatic
    def bresenham_plot_low(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        d = (2 * dy) - dx
        y = y0

        for x in range(x0, x1):
            if x % 32 == 0 and not self.src_pos[0] - 32 < x < self.src_pos[0] + 32:
                # pg.draw.rect(self.game.screen, (111, 1, 1), (x, y, 1, 1))
                for fog in self.game.fog.sprites():
                    if fog.rect.collidepoint(x, y):
                        fog.kill()
            if d > 0:
                y = y + yi
                d = d + (2 * (dy - dx))
            else:
                d = d + 2 * dy

    # noinspection PyMethodMayBeStatic
    def bresenham_plot_high(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        d = (2 * dx) - dy
        x = x0

        for y in range(y0, y1):
            if y % 32 == 0 and not self.src_pos[1] - 32 < y < self.src_pos[1] + 32:
                # pg.draw.rect(self.game.screen, (111, 1, 1), (x, y, 1, 1))
                for fog in self.game.fog.sprites():
                    if fog.rect.collidepoint(x, y):
                        fog.kill()
            if d > 0:
                x = x + xi
                d = d + (2 * (dx - dy))
            else:
                d = d + 2 * dx

    def update(self):
        self.game.all_sprites.update()
        self.game.camera.update(self.game.player.sprite)

    def render(self):
        self.game.screen.blit(self.game.map_img, self.game.camera.apply_rect(self.game.map_rect))
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply_sprite(sprite))
            if sprite.adjustable_layer:
                self.game.all_sprites.change_layer(sprite, sprite.rect.bottom)

        self.line_of_sight()

        if self.game.draw_debug:
            pg.draw.rect(self.game.screen, (255, 255, 255),
                         self.game.camera.apply_rect(self.game.player.sprite.rect), 1)
            groups = [self.game.npcs, self.game.entity, self.game.cleaner, self.game.obstacles, self.game.closed_doors,
                      self.game.opened_doors, self.game.interactables, self.game.items]
            for group in groups:
                for x in group:
                    pg.draw.rect(self.game.screen, (255, 255, 255), self.game.camera.apply_rect(x.rect), 1)
