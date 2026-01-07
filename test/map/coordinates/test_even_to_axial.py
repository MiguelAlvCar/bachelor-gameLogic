import unittest
import numpy as np
import numpy.testing as npt

from logic.map.coordinates.evenr_to_axial import evenr_to_axial

class TestEvenToAxial(unittest.TestCase):

    def test_even_to_axial1(self):
        evenr_coor = np.array([[1,1]])
        axial = evenr_to_axial(evenr_coor, 1)

        npt.assert_array_equal(axial, np.array([[0,1]]))

    def test_even_to_axial2(self):
        evenr_coor = np.array([[0,0]])
        axial = evenr_to_axial(evenr_coor, 1)

        npt.assert_array_equal(axial, np.array([[0,0]]))

    def test_even_to_axial3(self):
        evenr_coor = np.array([[1,0]])
        axial = evenr_to_axial(evenr_coor, 1)
        npt.assert_array_equal(axial, np.array([[-1,1]]))

    def test_even_to_axial4(self):
        evenr_coor = np.array([[1,0]])
        axial = evenr_to_axial(evenr_coor, 2)
        npt.assert_array_equal(axial, np.array([[0,1]]))

    def test_even_to_axial5(self):
        evenr_coor = np.array([[2,3]])
        axial = evenr_to_axial(evenr_coor, 3)
        npt.assert_array_equal(axial, np.array([[3,2]]))

    def test_even_to_axial6(self):
        evenr_coor = np.array([[0,0]])
        axial = evenr_to_axial(evenr_coor, 3)
        npt.assert_array_equal(axial, np.array([[1,0]]))

    def test_even_to_axial7(self):
        evenr_coor = np.array([[1,0]])
        axial = evenr_to_axial(evenr_coor, 3)
        npt.assert_array_equal(axial, np.array([[0,1]]))
