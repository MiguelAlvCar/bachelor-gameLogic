from numba import njit
import numpy as np


@njit(cache=True)
def axial_to_evenr(evenr_coordinates, map_height):
    col = evenr_coordinates[:, 0] - map_height // 2 + (evenr_coordinates[:, 1] + 1) // 2

    return np.column_stack((evenr_coordinates[:, 1], col))
