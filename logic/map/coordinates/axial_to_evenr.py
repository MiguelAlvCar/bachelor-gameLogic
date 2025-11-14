from numba import njit
import numpy as np


@njit(cache=True)
def axial_to_evenr(evenr_coordinates):
    parity = evenr_coordinates[1] & 1
    col = evenr_coordinates[0] + (evenr_coordinates[1] + parity) // 2
    row = evenr_coordinates[1]
    return np.array([row, col])
