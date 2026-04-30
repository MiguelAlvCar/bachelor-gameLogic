from numba import njit
from numba.typed import List
from numba import types
import numpy as np

from logic.map.geometry.find_direction_field import find_direction_field


@njit(cache=True)
def find_ring(position, radius):
    ring_fields = List.empty_list(types.int64[:])

    if radius == 0:
        ring_fields.append(position.copy())
        return ring_fields

    hex = position.astype(np.int16)
    for i in range(radius):
        hex = find_direction_field(0, hex)

    for i in range(6):
        for _ in range(radius):
            ring_fields.append(hex.astype(np.int64).copy())
            hex = find_direction_field((i + 2) % 6, hex)

    return ring_fields
