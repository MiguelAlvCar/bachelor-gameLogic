import numpy as np
from numba import njit

from logic.map.coordinates.evenr_to_axial import evenr_to_axial

@njit(cache=True)
def map_to_axial(width: int, height: int):
    result = np.empty((height, width, 2), dtype=np.int64)

    for row in range(height):
        for col in range(width):
            q, r = evenr_to_axial(row, col)
            result[row, col] = (q, r)

    return result
