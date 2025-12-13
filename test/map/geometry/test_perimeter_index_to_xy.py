import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.perimeter_index_to_xy import perimeter_index_to_xy


class TestPerimeterIndexToXY(unittest.TestCase):

    def test_perimeter_index_to_xy(self):
        result = perimeter_index_to_xy(3,5,6)
        self.assertTrue(result == (0,3))

    def test_perimeter_index_to_xy1(self):
        result = perimeter_index_to_xy(7,5,6)
        self.assertTrue(result == (3,4))

    def test_perimeter_index_to_xy2(self):
        result = perimeter_index_to_xy(11,5,6)
        self.assertTrue(result == (5,2))

    def test_perimeter_index_to_xy3(self):
        result = perimeter_index_to_xy(17,5,6)
        self.assertTrue(result == (1,0))

    def test_perimeter_index_to_xy4(self):
        result = perimeter_index_to_xy(0,5,6)
        self.assertTrue(result == (0,0))

    def test_perimeter_index_to_xy5(self):
        result = perimeter_index_to_xy(4,5,6)
        self.assertTrue(result == (0,4))

    def test_perimeter_index_to_xy6(self):
        result = perimeter_index_to_xy(9,5,6)
        self.assertTrue(result == (5,4))

    def test_perimeter_index_to_xy7(self):
        result = perimeter_index_to_xy(13,5,6)
        self.assertTrue(result == (5,0))
