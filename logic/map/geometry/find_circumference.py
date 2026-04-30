import numpy as np
from numba import njit
from numba.typed import List


@njit(cache=True)
def find_circumference(position, radius):
    circumference_fields = List()

    if radius == 0:
        circumference_fields.append(position)
        return circumference_fields

    values = [1, -1]
    for i in range(3):
        for value in values:
            for k in range(radius):
                coord = np.zeros(3, dtype=position.dtype)
                coord[i] = value * radius
                coord[(i+1) % 3] = - value * k
                coord[(i+2) % 3] = - (value * radius - value * k)

                coord[0:2] += position
                circumference_fields.append(coord[0:2])

    return circumference_fields
