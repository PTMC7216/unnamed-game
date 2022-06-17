import unittest
import logging
import pygame as pg
from src.tilemap import TiledMap


class TestMap(unittest.TestCase):

    logging.basicConfig(filename='../logs/test_map.log',
                        format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s',
                        level=logging.DEBUG)

    @classmethod
    def setUpClass(cls):
        cls.screen = pg.display.set_mode((1, 1))
        cls.map = TiledMap('../src/data/maps/map1.tmx')
        cls.map.make_map()

    def test_fog_dupes(self):
        coords = self.map.fog_xy
        logging.info(f"Total coords = {len(coords)}")

        dupes = [coord for coord in coords if coords.count(coord) > 1]
        logging.info(f"Total dupes = {len(dupes)}")

        unique_dupes = list(set(dupes))
        if unique_dupes:
            logging.debug(f"Dupe locations = {unique_dupes}")

        self.assertEqual(len(dupes), 0)


if __name__ == '__main__':
    unittest.main()
