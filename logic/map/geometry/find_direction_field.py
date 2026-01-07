import numpy as np
from numba import njit

@njit(cache=True)
def find_direction_field(direction, position):
    # comparing with the values of enum Directions
    if direction == 0:
        return np.array([position[0] - 1, position[1]], dtype=np.int16)
    elif direction == 1:
        return np.array([position[0], position[1] - 1], dtype=np.int16)
    elif direction == 2:
        return np.array([position[0] + 1, position[1] - 1], dtype=np.int16)
    elif direction == 3:
        return np.array([position[0] + 1, position[1]], dtype=np.int16)
    elif direction == 4:
        return np.array([position[0], position[1] + 1], dtype=np.int16)
    elif direction == 5:
        return np.array([position[0] - 1, position[1] + 1], dtype=np.int16)
    elif direction == 6:
        return np.array([position[0], position[1]], dtype=np.int16)
    else:
        raise ValueError(f"Incorrect direction: {direction}")

