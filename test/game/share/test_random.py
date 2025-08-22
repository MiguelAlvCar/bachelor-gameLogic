import unittest
import numpy as np

from logic.game.share.random import get_random_not_overlapping_positions

class TestRandom(unittest.TestCase):
    def test_get_random_all(self):
        positions = get_random_not_overlapping_positions(4, 2, 8)

        unique_rows = np.unique(positions, axis=0)
        self.assertEqual(len(unique_rows), len(positions), "Array has duplicate tuples")

        target_row = np.array([0, 0])
        found = any(np.all(row == target_row) for row in positions)
        self.assertTrue(found, msg=f"Target row {target_row} not found in array:\n{positions}")

        target_row = np.array([1, 3])
        found = any(np.all(row == target_row) for row in positions)
        self.assertTrue(found, msg=f"Target row {target_row} not found in array:\n{positions}")


    def test_get_random_with_two(self):
        positions = get_random_not_overlapping_positions(3, 3, 2)

        unique_rows = np.unique(positions, axis=0)
        self.assertEqual(len(unique_rows), len(positions), f"Array has duplicate tuples\n{positions}")

        lower_bound = 0
        upper_bound = 2

        # Check all values are >= lower_bound and <= upper_bound
        in_range = np.all((positions >= lower_bound) & (positions <= upper_bound))

        self.assertTrue(in_range, f"Not all values are within the specified range:\n{positions}")
