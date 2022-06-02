import pygame as pg
from .sprite import Sprite
from .items import Item
from src.allocs.stats import Stats
from src.states.pausewin import PauseWin
from src.states.notifywin import NotifyWin
from math import ceil


class Player(Sprite, Stats):
    def __init__(self, game, x, y):
        self.game = game
        self.adjustable_layer = True
        Sprite.__init__(self, game, x, y, self.game.player)

        self.name = "Nameless"
        self.title = ". . ."
        self.spritesheet = self.game.dcss2

        self.imgrect_center(self.spritesheet.image_at(1, 0, 1, 1))

        Stats.__init__(
            self,
            lv=1,
            hp=9,
            mp=0,
            strength=1,
            dexterity=1,
            agility=1,
            vitality=1,
            intelligence=1,
            charisma=1,
            alignment=5)

        self.combat_mode = False

        self.inventory = []
        self.inventory_size = 4

        self.dy = []
        self.dx = []

        self.anim_timer = pg.time.get_ticks()
        self.up = self.spritesheet.image_strip(0, 3, 1, 1, 3, -1)
        self.down = self.spritesheet.image_strip(0, 0, 1, 1, 3, -1)
        self.left = self.spritesheet.image_strip(0, 1, 1, 1, 3, -1)
        self.right = self.spritesheet.image_strip(0, 2, 1, 1, 3, -1)
        self.direction = []
        self.last_direction = None
        self.cooldown = 175
        self.frames = len(self.up) - 1
        self.frame = 0

        self.item_collision_kwargs = {"sprite": self.game.player.sprite,
                                      "group": self.game.items,
                                      "dokill": False}

        self.door_collision_kwargs = {"sprite": self.game.player.sprite,
                                      "group": self.game.closed_doors,
                                      "dokill": False,
                                      "collided": pg.sprite.collide_rect_ratio(1.1)}

        self.interactable_collision_kwargs = {"sprite": self.game.player.sprite,
                                              "group": self.game.interactables,
                                              "dokill": False}

        self.npc_collision_kwargs = {"sprite": self.game.player.sprite,
                                     "group": self.game.npcs,
                                     "dokill": False}

    def inv_add(self, item):
        if len(self.inventory) < 4:
            item.kill()
            self.inventory.append(item)
            NotifyWin(self.game, 1, f"{item.name} added to inventory.").enter_state()
        else:
            NotifyWin(self.game, 1, f"Inventory full.").enter_state()

    def interact(self):
        # TODO: shift key modifier for prioritizing certain actions during overlap
        if pg.sprite.spritecollide(**self.item_collision_kwargs):
            item = pg.sprite.spritecollide(**self.item_collision_kwargs)[-1]
            item.pickup()

        elif pg.sprite.spritecollide(**self.door_collision_kwargs):
            door = pg.sprite.spritecollide(**self.door_collision_kwargs)[-1]
            if door.key_req is None:
                door.open()
                NotifyWin(self.game, 1, f"Opened the {door.name.lower()}.").enter_state()
            else:
                NotifyWin(self.game, 1, f"{door.desc}.").enter_state()

        elif pg.sprite.spritecollide(**self.interactable_collision_kwargs):
            interactable = pg.sprite.spritecollide(**self.interactable_collision_kwargs)[-1]
            if interactable.subtype == "chest":
                interactable.open()

        elif pg.sprite.spritecollide(**self.npc_collision_kwargs):
            npc = pg.sprite.spritecollide(**self.npc_collision_kwargs)[-1]
            if self.combat_mode:
                self.attack(npc)
            else:
                npc.interact()

    def menu(self):
        self.game.select_sound.play()
        PauseWin(self.game).enter_state()

    def clear_stacks(self):
        self.dx.clear()
        self.dy.clear()
        self.direction.clear()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # TODO: display a quit confirmation window
                self.game.active = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKQUOTE:
                    self.game.draw_debug = not self.game.draw_debug
                if event.key == pg.K_ESCAPE:
                    self.menu()
                if event.key == pg.K_z:
                    self.interact()
                if event.key == pg.K_x:
                    self.menu()
                if event.key == pg.K_LSHIFT:
                    pass
                if event.key == pg.K_UP:
                    self.dy.insert(0, -self.movespeed)
                    self.direction.insert(0, 'up')
                if event.key == pg.K_DOWN:
                    self.dy.insert(0, self.movespeed)
                    self.direction.insert(0, 'down')
                if event.key == pg.K_LEFT:
                    self.dx.insert(0, -self.movespeed)
                    self.direction.insert(0, 'left')
                if event.key == pg.K_RIGHT:
                    self.dx.insert(0, self.movespeed)
                    self.direction.insert(0, 'right')

            elif event.type == pg.KEYUP:
                if event.key == pg.K_LSHIFT:
                    pass
                if event.key == pg.K_UP and self.dy:
                    self.dy.remove(-self.movespeed)
                    self.direction.remove('up')
                if event.key == pg.K_DOWN and self.dy:
                    self.dy.remove(self.movespeed)
                    self.direction.remove('down')
                if event.key == pg.K_LEFT and self.dx:
                    self.dx.remove(-self.movespeed)
                    self.direction.remove('left')
                if event.key == pg.K_RIGHT and self.dx:
                    self.dx.remove(self.movespeed)
                    self.direction.remove('right')

    def animations(self):
        if self.direction:
            current_time = pg.time.get_ticks()
            if current_time - self.anim_timer >= self.cooldown:
                self.frame += 2
                self.anim_timer = current_time
                if self.frame > self.frames:
                    self.frame = 0
            if self.direction[0] == 'up':
                self.last_direction = 'up'
                self.image = self.up[self.frame]
            if self.direction[0] == 'down':
                self.last_direction = 'down'
                self.image = self.down[self.frame]
            if self.direction[0] == 'left':
                self.last_direction = 'left'
                self.image = self.left[self.frame]
            if self.direction[0] == 'right':
                self.last_direction = 'right'
                self.image = self.right[self.frame]

        elif not self.direction:
            if self.last_direction is not None:
                if self.last_direction == 'up':
                    self.image = self.up[1]
                elif self.last_direction == 'down':
                    self.image = self.down[1]
                elif self.last_direction == 'left':
                    self.image = self.left[1]
                elif self.last_direction == 'right':
                    self.image = self.right[1]
                self.last_direction = None

    def collisions(self, axis):
        collision = pg.sprite.spritecollide(self, self.game.obstacles, False) or \
                    pg.sprite.spritecollide(self, self.game.closed_doors, False)

        if collision:
            if axis == 'y':
                if self.dy[0] > 0:
                    self.rect.y = collision[0].rect.top - self.rect.height
                if self.dy[0] < 0:
                    self.rect.y = collision[0].rect.bottom
                self.rect.y += 0

            if axis == 'x':
                if self.dx[0] > 0:
                    self.rect.x = collision[0].rect.left - self.rect.width
                if self.dx[0] < 0:
                    self.rect.x = collision[0].rect.right
                self.rect.x += 0

    def traversal(self):
        dt = self.game.dt_truncavg()
        if dt > 0.2:
            dt = self.game.dt_trunc()

        # rounding negatives up with ceil(), while leaving positives to round down.
        # this counteracts the movement issues caused by pygame's default truncation.
        if self.dy and self.dx:
            if self.dy[0] < 0:
                self.rect.y += ceil((self.dy[0] * 0.8) * dt)
                self.collisions('y')
            elif self.dy[0] > 0:
                self.rect.y += (self.dy[0] * 0.8) * dt
                self.collisions('y')
            if self.dx[0] < 0:
                self.rect.x += ceil((self.dx[0] * 0.8) * dt)
                self.collisions('x')
            elif self.dx[0] > 0:
                self.rect.x += (self.dx[0] * 0.8) * dt
                self.collisions('x')

        elif self.dy:
            if self.dy[0] < 0:
                self.rect.y += ceil(self.dy[0] * dt)
                self.collisions('y')
            elif self.dy[0] > 0:
                self.rect.y += self.dy[0] * dt
                self.collisions('y')

        elif self.dx:
            if self.dx[0] < 0:
                self.rect.x += ceil(self.dx[0] * dt)
                self.collisions('x')
            elif self.dx[0] > 0:
                self.rect.x += self.dx[0] * dt
                self.collisions('x')

    def update(self):
        self.check_events()
        self.animations()
        self.traversal()
