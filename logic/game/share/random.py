import numpy as np
import numpy.typing as npt
from numba import njit


#@njit(cache=True)
def get_random_not_overlapping_positions(width, height, number_of_positions):
    number_of_cells = width * height
    grid = np.empty((number_of_cells, 2), dtype=np.int16)

    for i in range(width):
        for j in range(height):
            grid[i * height + j] = np.array([i, j])


    is_in_position_idx = np.zeros(number_of_cells, dtype=np.bool)
    positions_idx = np.empty(number_of_positions, dtype=np.int16)
    counting = np.zeros(number_of_cells, dtype=np.int16)

    for i in range(number_of_positions):
        idx = np.random.randint(0, number_of_cells - i)
        idx = idx + counting[idx]

        while is_in_position_idx[idx]:
            idx += 1

        is_in_position_idx[idx] = True
        counting[idx:] +=  1

        positions_idx[i] = idx

    return grid[positions_idx]
