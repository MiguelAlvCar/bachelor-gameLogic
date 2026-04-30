import numpy as np
from numba import njit


@njit(cache=True)
def build_coords(width, height):
    coords = np.empty((width, height, 2), dtype=np.int32)
    for i in range(width):
        for j in range(height):
            coords[i, j, 0] = i
            coords[i, j, 1] = j
    return coords
