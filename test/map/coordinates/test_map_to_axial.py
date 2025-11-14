import unittest
import numpy as np
import numpy.testing as npt

from logic.map.coordinates.map_to_axial import map_to_axial


class TestMapToAxial(unittest.TestCase):

    def test_map_to_axial(self):
        axial_coords = map_to_axial(4,3)

        npt.assert_array_equal(axial_coords[1,1,:], np.array([0,1]))
        npt.assert_array_equal(axial_coords[0,0,:], np.array([0,0]))
        npt.assert_array_equal(axial_coords[1,0,:], np.array([-1,1]))
        npt.assert_array_equal(axial_coords[0,1,:], np.array([1,0]))
        npt.assert_array_equal(axial_coords[2,3,:], np.array([2,2]))
