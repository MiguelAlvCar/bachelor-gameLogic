import unittest
import numpy as np
import numpy.testing as npt

from logic.map.geometry.calculate_distance import calculate_distance

class TestCalculateDistance(unittest.TestCase):

    def test_calculate_distance1(self):
        result = calculate_distance(np.array([0,0]), np.array([1,0]))
        self.assertEqual(result, 1)

    def test_calculate_distance2(self):
        result = calculate_distance(np.array([0,1]), np.array([0,0]))
        self.assertEqual(result, 1)

    def test_calculate_distance3(self):
        result = calculate_distance(np.array([0,1]), np.array([1,0]))
        self.assertEqual(result, 1)

    def test_calculate_distance4(self):
        result = calculate_distance(np.array([0,1]), np.array([-1,0]))
        self.assertEqual(result, 2)

    def test_calculate_distance5(self):
        result = calculate_distance(np.array([0,2]), np.array([-2,0]))
        self.assertEqual(result, 4)

    def test_calculate_distance6(self):
        result = calculate_distance(np.array([0,2]), np.array([2,0]))
        self.assertEqual(result, 2)

    def test_calculate_distance7(self):
        result = calculate_distance(np.array([0,2]), np.array([0,0]))
        self.assertEqual(result, 2)

    def test_calculate_distance_vectorized(self):
        # Test with multiple coordinate pairs at once
        origins = np.array([[0, 0], [0, 1], [0, 2]])
        ends = np.array([[1, 0], [1, 0], [-2, 0]])
        result = calculate_distance(origins, ends)
        expected = np.array([1, 1, 4])
        npt.assert_array_equal(result, expected)

    def test_calculate_distance_vectorized_single_origin(self):
        # Test with multiple coordinate pairs at once
        origins = np.array([0,1])
        ends = np.array([[-1,0], [0,0]])
        result = calculate_distance(origins, ends)
        expected = np.array([2, 1])
        npt.assert_array_equal(result, expected)

