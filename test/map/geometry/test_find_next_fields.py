import unittest
import numpy as np
import numpy.testing as npt

from logic.map.map import Map


class TestFindNextFields(unittest.TestCase):

    def test_find_next_fields1(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([2, 2]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[3, 2],[3, 1],[2, 3]]))

    def test_find_next_fields2(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([1, 8]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[2, 7],[1, 7]]))

    def test_find_next_fields3(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([0, 0]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([]))

    def test_find_next_fields4(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([9, 7]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[ 8,  7],[10,  6],[ 9,  6]]))

    def test_find_next_fields5(self):
        map = Map(10, 7)
        next_fields = map.find_next_fields(np.array([6, 0]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[7, 0],[5, 0],[5, 1],[6, 1]]))

    def test_find_next_fields6(self):
        map = Map(10, 9)
        next_fields = map.find_next_fields(np.array([6, 0]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[7, 0],[5, 0],[5, 1],[6, 1]]))

    def test_find_next_fields7(self):
        map = Map(10, 9)
        next_fields = map.find_next_fields(np.array([9, 6]))
        next_fields = np.array(next_fields, dtype=np.int16)
        npt.assert_array_equal(next_fields, np.array([[10,  6],[ 8,  6],[ 8,  7],[10,  5],[ 9,  5],[ 9, 7]]))
