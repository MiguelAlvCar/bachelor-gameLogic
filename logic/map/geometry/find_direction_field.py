import numpy as np
from numba import njit


# invalid position are marked with the value of the first coordinate '-1'
@njit(cache=True)
def find_direction_field(direction, position, width, height):
    if direction == 0:
        if position[1] == 0:
            return np.array([-1, -1])
        else:
            return np.array([position[0], position[1]-1])

    elif direction == 1:
        if position[0] % 2 == 0:
            return np.array([position[0]-1, position[1]])
        else:
            if position[1] == 0:
                return np.array([-1, -1])
            return np.array([position[0]-1, position[1]-1])

    elif direction == 2:
        if position[0] % 2 == 0:
            if position[1] == width - 1:
                return np.array([-1, -1])
            return np.array([position[0]-1, position[1]+1])
        else:
            return np.array([position[0]-1, position[1]])

    elif direction == 3:
        if position[1] == width - 1:
            return np.array([-1, -1])
        else:
            return np.array([position[0], position[1]+1])

    elif direction == 4:
        if position[0] == height - 1:
            return np.array([-1, -1])
        if position[0] % 2 == 0:
            if position[1] == width - 1:
                return np.array([-1, -1])
            return np.array([position[0]+1, position[1]+1])
        else:
            return np.array([position[0]+1, position[1]])

    elif direction == 5:
        if position[0] == height - 1:
            return np.array([-1, -1])
        if position[0] % 2 == 0:
            return np.array([position[0]+1, position[1]])
        else:
            if position[1] == 0:
                return np.array([-1, -1])
            return np.array([position[0]+1, position[1]-1])
