import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.make_get_neighbors import make_get_neighbors
from logic.game.chasing_game.chasing_game import ChasingGame


class TestMakeGetNeighbors(unittest.TestCase):

    def test_make_get_neighbors1(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        neighbors = get_neighbors(np.array([1, 1], dtype=np.int64))
        self.assertEqual(len(neighbors), 0)

    def test_make_get_neighbors2(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        neighbors = get_neighbors(np.array([6, 0], dtype=np.int64))

        self.assertEqual(len(neighbors), 4)
        npt.assert_array_equal(neighbors[0], np.array([7, 0]))
        npt.assert_array_equal(neighbors[1], np.array([5, 0]))
        npt.assert_array_equal(neighbors[2], np.array([5, 1]))
        npt.assert_array_equal(neighbors[3], np.array([6, 1]))
