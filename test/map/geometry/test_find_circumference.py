import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.find_circumference import _find_directional_fields, find_circumference


class TestFindDirectionField(unittest.TestCase):

    def test_find_directional_fields(self):
        directional_fields = _find_directional_fields(np.array([4, 4]), 9, 9, 2)

        npt.assert_array_equal(directional_fields[0], np.array([4, 2]))
        npt.assert_array_equal(directional_fields[1], np.array([2, 3]))
        npt.assert_array_equal(directional_fields[2], np.array([2, 5]))
        npt.assert_array_equal(directional_fields[3], np.array([4, 6]))
        npt.assert_array_equal(directional_fields[4], np.array([6, 5]))
        npt.assert_array_equal(directional_fields[5], np.array([6, 3]))

    def test_find_directional_fields1(self):
        directional_fields = _find_directional_fields(np.array([4, 4]), 9, 9, 3)

        npt.assert_array_equal(directional_fields[0], np.array([4, 1]))
        npt.assert_array_equal(directional_fields[1], np.array([1, 3]))
        npt.assert_array_equal(directional_fields[2], np.array([1, 6]))
        npt.assert_array_equal(directional_fields[3], np.array([4, 7]))
        npt.assert_array_equal(directional_fields[4], np.array([7, 6]))
        npt.assert_array_equal(directional_fields[5], np.array([7, 3]))

    def test_find_directional_fields2(self):
        directional_fields = _find_directional_fields(np.array([1, 1]), 9, 9, 3)

        self.assertTrue(directional_fields[0][0] < 0)
        self.assertTrue(directional_fields[1][0] < 0)
        self.assertTrue(directional_fields[2][0] < 0)
        npt.assert_array_equal(directional_fields[3], np.array([1, 4]))
        npt.assert_array_equal(directional_fields[4], np.array([4, 2]))
        self.assertTrue(directional_fields[5][0] < 0)

    def test_find_directional_fields3(self):
        directional_fields = _find_directional_fields(np.array([8, 8]), 9, 9, 3)

        npt.assert_array_equal(directional_fields[0], np.array([8, 5]))
        npt.assert_array_equal(directional_fields[1], np.array([5, 7]))
        self.assertTrue(directional_fields[2][0] < 0)
        self.assertTrue(directional_fields[3][0] < 0)
        self.assertTrue(directional_fields[4][0] < 0)
        self.assertTrue(directional_fields[5][0] < 0)

    def test_find_circumference(self):
        circumference = find_circumference(np.array([4, 4]), 9, 9, 1)

        npt.assert_array_equal(circumference[0], np.array([4, 3]))
        npt.assert_array_equal(circumference[1], np.array([3, 4]))
        npt.assert_array_equal(circumference[2], np.array([3, 5]))
        npt.assert_array_equal(circumference[3], np.array([4, 5]))
        npt.assert_array_equal(circumference[4], np.array([5, 5]))
        npt.assert_array_equal(circumference[5], np.array([5, 4]))

    def test_find_circumference1(self):
        circumference = find_circumference(np.array([4, 4]), 9, 9, 2)

        npt.assert_array_equal(circumference[0], np.array([4, 2]))
        npt.assert_array_equal(circumference[3], np.array([2, 4]))
        npt.assert_array_equal(circumference[4], np.array([2, 5]))
        npt.assert_array_equal(circumference[6], np.array([4, 6]))
        npt.assert_array_equal(circumference[9], np.array([6, 4]))
        npt.assert_array_equal(circumference[10], np.array([6, 3]))

    def test_find_circumference2(self):
        circumference = find_circumference(np.array([4, 4]), 9, 9, 0)
        self.assertEqual(len(circumference), 1)
        npt.assert_array_equal(circumference[0], np.array([4, 4]))
