import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.find_valid_circumference import find_valid_circumference
from logic.map.map import Map


class TestFindDirectionField(unittest.TestCase):

    def test_find_circumference(self):

        map = Map(6,7)

        circumference = find_valid_circumference(np.array([3, 0]), map.playable_fields, 1)

        npt.assert_array_equal(circumference[0], np.array([4, 0]))
        npt.assert_array_equal(circumference[1], np.array([2, 1]))
        npt.assert_array_equal(circumference[2], np.array([3, 1]))
        self.assertTrue(len(circumference) == 3)

    def test_find_circumference1(self):

        map = Map(6,8)

        circumference = find_valid_circumference(np.array([0, 0]), map.playable_fields, 1)

        self.assertTrue(len(circumference) == 0)

    def test_find_circumference2(self):

        map = Map(6,8)

        circumference = find_valid_circumference(np.array([4, 7]), map.playable_fields, 1)

        npt.assert_array_equal(circumference[0], np.array([5, 7]))
        npt.assert_array_equal(circumference[1], np.array([3, 7]))
        npt.assert_array_equal(circumference[2], np.array([5, 6]))
        npt.assert_array_equal(circumference[3], np.array([4, 6]))
        self.assertTrue(len(circumference) == 4)

    def test_find_circumference3(self):

        map = Map(6,8)

        circumference = find_valid_circumference(np.array([4, 4]), map.playable_fields, 2)

        npt.assert_array_equal(circumference[0], np.array([6, 4]))
        npt.assert_array_equal(circumference[3], np.array([2, 5]))
        npt.assert_array_equal(circumference[10], np.array([4, 6]))

        self.assertTrue(len(circumference) == 12)

    def test_find_circumference4(self):
        map = Map(6,8)

        circumference = find_valid_circumference(np.array([4, 4]), map.playable_fields, 0)

        self.assertEqual(len(circumference), 1)
        npt.assert_array_equal(circumference[0], np.array([4, 4]))
