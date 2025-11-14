import unittest
import numpy as np
import numpy.testing as npt

from logic.map.map import Map


class TestFindNextFields(unittest.TestCase):

    def test_find_next_fields1(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([2, 2]))
        npt.assert_array_equal(next_fields, np.array([[2,1],[1,2],[1,3],[2,3],[3,3],[3,2]]))

    def test_find_next_fields2(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([1, 8]))
        npt.assert_array_equal(next_fields, np.array([[1,7],[0,7],[0,8],[1,9],[2,8],[2,7]]))

    def test_find_next_fields3(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([0, 0]))
        npt.assert_array_equal(next_fields, np.array([[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0]]))

    def test_find_next_fields4(self):
        map = Map(10, 8)
        next_fields = map.find_next_fields(np.array([7, 9]))
        npt.assert_array_equal(next_fields, np.array([[7,8],[6,8],[6,9],[-1,10],[-1,9],[-1,8]]))

    def test_find_next_fields5(self):
        map = Map(10, 7)
        next_fields = map.find_next_fields(np.array([6, 0]))
        npt.assert_array_equal(next_fields, np.array([[-1,-1],[5,0],[5,1],[6,1],[-1,1],[-1,0]]))

    def test_find_next_fields6(self):
        map = Map(10, 9)
        next_fields = map.find_next_fields(np.array([6, 0]))
        npt.assert_array_equal(next_fields, np.array([[-1,-1],[5,0],[5,1],[6,1],[7,1],[7,0]]))

    def test_find_next_fields7(self):
        map = Map(10, 9)
        next_fields = map.find_next_fields(np.array([6, 9]))
        npt.assert_array_equal(next_fields, np.array([[6,8],[5,9],[-1,10],[-1,10],[-1,10],[7,9]]))
