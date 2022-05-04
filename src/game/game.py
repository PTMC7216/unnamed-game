import pygame as pg
import utils
import states
import sprites
import tilemap
from time import time


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
        self.selector_sound.set_volume(0.5)
        self.select_sound = pg.mixer.Sound('./data/sounds/select.ogg')

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

        # sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = pg.sprite.GroupSingle()
        self.npcs = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.closed_doors = pg.sprite.Group()
        self.open_doors = pg.sprite.Group()
        self.interactables = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # tiles
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                sprites.Player(self, tile_object.x, tile_object.y)
            if tile_object.type == 'npc':
                sprites.NPC(self, tile_object.x, tile_object.y, tile_object.name)
            if tile_object.type == 'obstacle':
                sprites.Obstacles(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.type == 'door':
                sprites.Door(self, tile_object.x, tile_object.y, tile_object.name)
            if tile_object.type == 'interactable':
                sprites.Interactable(self, tile_object.x, tile_object.y, tile_object.name)
            if tile_object.type == 'item':
                sprites.Item(self, tile_object.x, tile_object.y, tile_object.name)

        # camera & rect borders
        self.camera = tilemap.Camera(self)
        self.draw_debug = False

        # delta time
        self.clk = pg.time.Clock()
        self.time_base = 0
        self.dt = 0

    def get_dt(self):
        now = time()
        self.dt = now - self.time_base
        self.time_base = now

    def update(self):
        self.get_dt()
        self.state_stack[-1].update()

    def render(self):
        self.state_stack[-1].render()
        pg.display.update()
        self.clk.tick(self.framerate)

    def loop(self):
        while self.active:
            self.update()
            self.render()
