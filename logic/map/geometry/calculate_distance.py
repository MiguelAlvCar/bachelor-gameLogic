import numpy as np
from numba import njit


@njit(cache=True)
def calculate_distance(axial_origin, axial_end):
    dx = np.abs(axial_origin[..., 0] - axial_end[..., 0])
    dy = np.abs(axial_origin[..., 1] - axial_end[..., 1])
    dz = np.abs(axial_end[..., 0] + axial_end[..., 1] - axial_origin[..., 0] - axial_origin[..., 1])
    return np.maximum(np.maximum(dx, dy), dz)
