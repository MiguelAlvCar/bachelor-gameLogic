import unittest
import numpy as np
import numpy.testing as npt

from logic.game.several_units_game.generate_units.generate_deployment_areas import generate_deployment_areas
from logic.map.map import Map


class TestGenerateDeployment(unittest.TestCase):

    def test_generate1(self):
        map = Map(10, 8)
        result = generate_deployment_areas(map)

        self.assertEqual(result[0].shape, (20, 2))
        self.assertEqual(result[1].shape, (20, 2))

        self.assertEqual(len(np.unique(result[0], axis=0)), 20)
        self.assertEqual(len(np.unique(result[1], axis=0)), 20)
