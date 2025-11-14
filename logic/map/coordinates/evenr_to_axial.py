from numba import njit
import numpy as np

@njit(cache=True)
def evenr_to_axial(evenr_coordinates):
    parity = evenr_coordinates[0] & 1
    q = evenr_coordinates[1] - (evenr_coordinates[0] + parity) // 2
    return np.array([q, evenr_coordinates[0]])
