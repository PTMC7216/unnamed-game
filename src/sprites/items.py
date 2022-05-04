import pygame as pg


class Item:
    def __init__(self, game, x, y, item_name):
        self.game = game

        item_dict = {
            "Brass Key": BrassKey
        }

        item_dict[item_name](game, x, y)


class ItemCon(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = -1
        self.adjustable_layer = False
        pg.sprite.Sprite.__init__(self, self.game.items, self.game.all_sprites)

    def pickup(self):
        # TODO: add notifier state, or rect, to display pickup message
        self.kill()
        self.game.player.sprite.inventory.append(self)
        print(f"{self.name} added to inventory.")


class BrassKey(ItemCon):
    def __init__(self, game, x, y):
        ItemCon.__init__(self, game)

        self.image = self.game.extra1.image_at(4, 3, 1, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = "Brass Key"
        self.desc = "An ordinary brass key."
