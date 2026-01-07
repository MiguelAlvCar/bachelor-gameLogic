import unittest

from logic.game.comp_chasing_game.generate_terrain.generate_hills import generate_hills
from logic.map.map import Map


class TestGenerateHills(unittest.TestCase):

    def test_generate_hills(self):
        map = Map(even_width=5, height=5)
        generate_hills(map, 0.2)

