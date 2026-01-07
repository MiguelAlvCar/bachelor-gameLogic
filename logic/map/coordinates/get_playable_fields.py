import numpy as np
from numba import njit


@njit(cache=True)
def get_playable_fields(height, axial_width):
    even_width = axial_width - height // 2

    coords = np.empty((even_width, height, 2), dtype=np.int16)
    for i in range(even_width):
        for j in range(height):
            coords[i, j, 0] = i
            coords[i, j, 1] = j

    offsets = np.arange((height // 2), -1, -1)
    offsets = np.repeat(offsets, 2)

    coords[:,:,0] += offsets[1:height+1]
    coords = coords.reshape(-1, 2)

    playable_fields = np.zeros((axial_width, height), dtype=np.bool_)
    for i in range(coords.shape[0]):
        playable_fields[coords[i, 0], coords[i, 1]] = True

    return playable_fields
