import unittest
import numpy as np
import numpy.testing as npt

from logic.map.coordinates.axial_to_evenr import axial_to_evenr


class TestEvenToAxial(unittest.TestCase):

    def test_axial_to_evenr1(self):
        axial = np.array([[0,1]])
        evenr = axial_to_evenr(axial, 1)

        npt.assert_array_equal(evenr, np.array([[1,1]]))

    def test_axial_to_evenr2(self):
        axial = np.array([[0,0]])
        evenr = axial_to_evenr(axial, 1)

        npt.assert_array_equal(evenr, np.array([[0,0]]))

    def test_axial_to_evenr3(self):
        axial = np.array([[-1,1]])
        evenr = axial_to_evenr(axial, 1)
        npt.assert_array_equal(evenr, np.array([[1,0]]))

    def test_axial_to_evenr4(self):
        axial = np.array([[0,1]])
        evenr = axial_to_evenr(axial, 2)
        npt.assert_array_equal(evenr, np.array([[1,0]]))

    def test_axial_to_evenr5(self):
        axial = np.array([[3,2]])
        evenr = axial_to_evenr(axial, 3)
        npt.assert_array_equal(evenr, np.array([[2,3]]))

    def test_even_to_axial6(self):
        axial = np.array([[1,0]])
        evenr = axial_to_evenr(axial, 3)
        npt.assert_array_equal(evenr, np.array([[0,0]]))

    def test_even_to_axial7(self):
        axial = np.array([[0,1]])
        evenr = axial_to_evenr(axial, 3)
        npt.assert_array_equal(evenr, np.array([[1,0]]))
