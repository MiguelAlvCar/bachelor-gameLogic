from numba import njit
import numpy as np


@njit(cache=True)
def get_strided_mask(width, height, stride):

    coords = np.empty((width, height, 2), dtype=np.int16)
    for i in range(width):
        for j in range(height):
            coords[i, j, 1] = i
            coords[i, j, 0] = j

    coords = coords.reshape(-1, 2)

    mask = (coords[:,0] % stride == 0) & (coords[:,1] % stride == 0)

    return mask.reshape(width, height)



