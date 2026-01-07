import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.find_hex_line import find_hex_line
from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.coordinates.axial_to_evenr import axial_to_evenr

class TestFindLine(unittest.TestCase):

    def test_find_find_line(self):
        axial_origin = np.array([-5,0])
        axial_end = np.array([0,-5])
        result = find_hex_line(axial_origin, axial_end)

        npt.assert_array_equal(result, np.array([[-5,  0], [-4, -1], [-3, -2], [-2, -3], [-1, -4], [ 0, -5]]))

    def test_find_find_line1(self):
        even_origin = np.array([[0,0]])
        even_end = np.array([[0,5]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]))

    def test_find_find_line2(self):
        even_origin = np.array([[0,0]])
        even_end = np.array([[5,0]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]))

    def test_find_find_line3(self):
        even_origin = np.array([[1,0]])
        even_end = np.array([[1,5]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]))

    def test_find_find_line4(self):
        even_origin = np.array([[0,0]])
        even_end = np.array([[2,2]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[0, 0], [1, 1], [1, 2], [2, 2]]))

    def test_find_find_line5(self):
        even_origin = np.array([[0,0]])
        even_end = np.array([[3,3]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[0, 0], [1, 1], [2, 1], [2, 2], [3, 3]]))

    def test_find_find_line6(self):
        even_origin = np.array([[1,1]])
        even_end = np.array([[3,3]])

        axial_origin = evenr_to_axial(even_origin, 6)[0]
        axial_end = evenr_to_axial(even_end, 6)[0]

        result = find_hex_line(axial_origin, axial_end)
        result = np.array(result, dtype=np.int16)

        even_result = axial_to_evenr(result, 6)

        npt.assert_array_equal(even_result, np.array([[1, 1], [2, 1], [2, 2], [3, 3]]))
