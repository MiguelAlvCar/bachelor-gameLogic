import unittest

from logic.map.geometry.get_strided_mask import get_strided_mask


class TestGetStrideField(unittest.TestCase):

    def test_get_stride_fields1(self):
        stride_fields = get_strided_mask(5, 5, 2)

    def test_get_stride_fields2(self):
        stride_fields = get_strided_mask(7, 7, 3)
