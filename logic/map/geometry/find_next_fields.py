import numpy as np
from numba import njit


# invalid position are marked with the value of the first coordinate '-1'
@njit(cache=True)
def find_next_fields(position, width, height):
    if position[0] % 2 == 0:
        next_fields =  np.array([[position[0], position[1]-1],
                            [position[0]-1, position[1]],
                            [position[0]-1, position[1]+1],
                            [position[0], position[1]+1],
                            [position[0]+1, position[1]+1],
                            [position[0]+1, position[1]]])
        if position[1] == 0:
            next_fields[0,0] = -1
        elif position[1] == width - 1:
            next_fields[2:5,0] = -1
    else:
        next_fields =  np.array([[position[0], position[1]-1],
                            [position[0]-1, position[1]-1],
                            [position[0]-1, position[1]],
                            [position[0], position[1]+1],
                            [position[0]+1, position[1]],
                            [position[0]+1, position[1]-1]])
        if position[1] == 0:
            next_fields[0:2,0] = -1
            next_fields[5,0] = -1
        elif position[1] == width - 1:
            next_fields[3,0] = -1

    if position[0] == height - 1:
        next_fields[4:, 0] = -1

    return next_fields
