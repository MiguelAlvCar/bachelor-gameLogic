import unittest
import numpy as np

from logic.map.geometry.a_star import a_star
from logic.map.geometry.make_get_neighbors import make_get_neighbors
from logic.game.chasing_game.chasing_game import ChasingGame
from logic.map.geometry.calculate_distance import calculate_distance


class TestAStart(unittest.TestCase):

    def test_a_start1(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        movement_cost = np.ones((14,8))

        came_from, cost_so_far = a_star(movement_cost, np.array([2,3]), np.array([11,3]), calculate_distance, get_neighbors)
        last = came_from[tuple(np.array([11,3]))]
        self.assertEqual(last, (10,3))
        last = came_from[last]
        self.assertEqual(last, (9,3))
        last = came_from[last]
        self.assertEqual(last, (8,3))

        self.assertEqual(cost_so_far[tuple(np.array([11,3]))], 9)

    def test_a_start2(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        movement_cost = np.ones((14,8))
        movement_cost[10,3] = 9

        came_from, cost_so_far = a_star(movement_cost, np.array([2,3]), np.array([11,3]), calculate_distance, get_neighbors)
        last = came_from[tuple(np.array([11,3]))]
        self.assertEqual(last, (10,4))
        last = came_from[last]
        self.assertEqual(last, (9,4))
        last = came_from[last]
        self.assertEqual(last, (9,3))

        self.assertEqual(cost_so_far[tuple(np.array([11,3]))], 10)


    def test_a_start3(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        movement_cost = np.ones((14,8))

        came_from, cost_so_far = a_star(movement_cost, np.array([0,7]), np.array([3,5]), calculate_distance, get_neighbors)
        last = came_from[tuple(np.array([3,5]))]
        self.assertEqual(last, (2,5))
        last = came_from[last]
        self.assertEqual(last, (1,6))
        last = came_from[last]
        self.assertEqual(last, (0,7))

        self.assertEqual(cost_so_far[tuple(np.array([3,5]))], 3)


    def test_a_start4(self):

        game = ChasingGame(None)
        get_neighbors = make_get_neighbors(game.map.playable_fields)
        movement_cost = np.ones((14,8))
        movement_cost[[2, 2, 3], [5, 6, 6]] = 9

        came_from, cost_so_far = a_star(movement_cost, np.array([0,7]), np.array([3,5]), calculate_distance, get_neighbors)
        last = came_from[tuple(np.array([3,5]))]
        self.assertEqual(last, (3,4))
        last = came_from[last]
        self.assertEqual(last, (2,4))
        last = came_from[last]
        self.assertEqual(last, (1,5))

        self.assertEqual(cost_so_far[tuple(np.array([3,5], dtype=np.int64))], 5)
