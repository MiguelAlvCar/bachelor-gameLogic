import unittest

from logic.game.comp_chasing_game.generate_terrain.generate_forests import generate_forests
from logic.map.map import Map


class TestGenerateForest(unittest.TestCase):

    def test_generate_forest(self):
        map = Map(width=5, height=5)
        generate_forests(map, 0.2)
