from numba import njit
import numpy as np

@njit(cache=True)
def evenr_to_axial(evenr_coordinates, map_height):
    q = evenr_coordinates[:, 1] - (evenr_coordinates[:, 0] + 1) // 2

    # to not get negativ axial coordinates
    q += map_height // 2
    return np.column_stack((q, evenr_coordinates[:, 0]))
