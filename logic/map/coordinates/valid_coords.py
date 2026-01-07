import numpy as np
from numba import njit


@njit(cache=True)
def valid_coords(coords, mask):
    valid_fields = np.zeros(coords.shape[0], dtype=np.bool_)
    for i in range(coords.shape[0]):
        valid_fields[i] = coords[i,0] >= 0 and coords[i,1] >= 0 and coords[i,1] < mask.shape[1] and \
              coords[i,0] < mask.shape[0] and mask[coords[i,0], coords[i,1]]

    return valid_fields
