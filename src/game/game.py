import pygame as pg
import utils
import states
import sprites
import tilemap
from time import time
from statistics import mean


class Game:
    def __init__(self):
        pg.display.set_caption('Unnamed')
        pg.display.set_icon(pg.image.load('./data/images/icondefault.png'))

        self.tilesize = 32
        self.framerate = 60
        self.screen_res = {"x": 800, "y": 600}
        self.screen = pg.display.set_mode((self.screen_res["x"], self.screen_res["y"]))
        self.active = True

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 155))

        # main menu music
        pg.mixer.init()
        pg.mixer.music.load('./data/music/ominous1.ogg')
        pg.mixer.music.play(-1, 0.0, 10000)

        # general sounds
        self.selector_sound = pg.mixer.Sound('./data/sounds/selector.ogg')
        self.select_sound = pg.mixer.Sound('./data/sounds/select.ogg')

        # volume
        self.selector_sound.set_volume(0.0)
        self.select_sound.set_volume(0.0)

        # general spritesheets
        self.dcss1 = utils.Spritesheet(self, 'dcss1.png')
        self.dcss2 = utils.Spritesheet(self, 'dcss2.png')
        self.extra1 = utils.Spritesheet(self, 'extra1.png')

        # state stack
        self.state_stack = []
        self.state_stack.append(states.MainMenu(self))

        # maps
        self.map = tilemap.TiledMap('map1.tmx')
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = pg.sprite.GroupSingle()
        self.entity = pg.sprite.GroupSingle()
        self.cleaner = pg.sprite.GroupSingle()
        self.relocators = []
        self.npcs = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.closed_doors = pg.sprite.Group()
        self.opened_doors = pg.sprite.Group()
        self.interactables = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # tiles
        for tile in self.map.tmxdata.objects:
            if tile.name == 'player':
                sprites.Player(self, tile.x, tile.y)
            if tile.type == 'entity':
                sprites.Entity(self, tile.x, tile.y, tile.width, tile.height)
            if tile.type == 'cleaner':
                sprites.Cleaner(self, tile.x, tile.y, tile.width, tile.height)
            if tile.type == 'relocator':
                sprites.Relocator(self, tile.x, tile.y, tile.width, tile.height, tile.name)
            if tile.type == 'npc':
                sprites.NPC(self, tile.x, tile.y, tile.name)
            if tile.type == 'obstacle':
                sprites.Obstacles(self, tile.x, tile.y, tile.width, tile.height)
            if tile.type == 'door':
                sprites.Door(self, tile.x, tile.y, tile.name)
            if tile.type == 'interactable':
                sprites.Interactable(self, tile.x, tile.y, tile.name)
            if tile.type == 'item':
                sprites.Item(self, tile.x, tile.y, tile.name)

        # camera & rect borders
        self.camera = tilemap.Camera(self)
        self.draw_debug = False

        # delta time
        self.clk = pg.time.Clock()
        self.time_base = 0
        self.dt = 0
        self.dt_i = 0
        self.dt_arr = [0] * 60

    def update_dt(self):
        now = time()
        self.dt = now - self.time_base
        self.time_base = now

    def update_dt_avg(self):
        self.dt_i += 1
        if self.dt_i >= 60:
            self.dt_i = 0
        self.dt_arr[self.dt_i] = self.dt

    def dt_trunc(self):
        return utils.funcs.truncate(self.dt, 3)

    def dt_truncavg(self):
        return utils.funcs.truncate(mean(self.dt_arr), 3)

    def update(self):
        self.update_dt()
        self.update_dt_avg()
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render()
        pg.display.update()
        self.clk.tick(self.framerate)

    def loop(self):
        while self.active:
            self.update()
            self.render()
