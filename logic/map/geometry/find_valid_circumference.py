import numpy as np
from numba import njit
from numba.typed import List
from numba import types

from logic.map.coordinates.valid_coord import valid_coord


@njit(cache=True)
def find_valid_circumference(position, mask, radius):
    circumference_fields = List.empty_list(types.int64[:])

    if radius == 0:
        circumference_fields.append(position)
        return circumference_fields

    values = [1, -1]
    for i in range(3):
        for value in values:
            for k in range(radius):
                coord = np.zeros(3, dtype=np.int64)
                coord[i] = value * radius
                coord[(i+1) % 3] = - value * k
                coord[(i+2) % 3] = - (value * radius - value * k)

                coord[0:2] += position

                if valid_coord(coord, mask):
                    circumference_fields.append(coord[0:2])

    return circumference_fields
