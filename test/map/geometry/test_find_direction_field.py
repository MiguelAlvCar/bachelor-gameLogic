import unittest
import numpy as np
import numpy.testing as npt

from logic.map.map import Map


class TestFindDirectionField(unittest.TestCase):

    def test_find_direction_field1(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(0, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([1,2]))

    def test_find_direction_field3(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(3, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([3,2]))

    def test_find_direction_field5(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(1, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([2,1]))

    def test_find_direction_field6(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(2, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([3,1]))

    def test_find_direction_field7(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(4, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([2,3]))

    def test_find_direction_field8(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(5, np.array([2, 2]))
        npt.assert_array_equal(next_field, np.array([1,3]))

    def test_find_direction_field9(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(1, np.array([1, 1]))
        npt.assert_array_equal(next_field, np.array([1,0]))

    def test_find_direction_field10(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(2, np.array([1, 1]))
        npt.assert_array_equal(next_field, np.array([2,0]))

    def test_find_direction_field11(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(4, np.array([1, 1]))
        npt.assert_array_equal(next_field, np.array([1,2]))

    def test_find_direction_field12(self):
        map = Map(10, 8)
        next_field = map.find_direction_field(5, np.array([1, 1]))
        npt.assert_array_equal(next_field, np.array([0,2]))

    def test_find_direction_inverse_for_neighbors(self):
        map = Map(10, 8)
        origin = np.array([2, 2], dtype=np.int16)

        for direction in range(6):
            target = map.find_direction_field(direction, origin)
            found_direction = map.find_direction(origin, target)
            self.assertEqual(found_direction, direction)

    def test_find_direction_raises_for_non_neighbors(self):
        map = Map(10, 8)

        with self.assertRaises(ValueError):
            map.find_direction(np.array([2, 2], dtype=np.int16), np.array([4, 2], dtype=np.int16))
