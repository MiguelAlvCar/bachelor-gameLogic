import numpy as np
from numba import njit
from numba.typed import List
from numba import types

from logic.map.geometry.find_direction_field import find_direction_field


@njit(cache=True)
def find_circumference(position, width, height, radius):
    circumference_fields = List.empty_list(types.int64[:])

    if radius == 0:
        circumference_fields.append(position)
        return circumference_fields

    directional_fields = _find_directional_fields(position, width, height, radius)

    for direction in range(6):
        directional_field = directional_fields[direction]
        next_field = directional_fields[(direction + 1) % 6]

        while not (directional_field[0] == next_field[0] and directional_field[1] == next_field[1]):

            if directional_field[0] < 0:
                raise ValueError(f"Cannot find circumference: out of bounds: " +
                                 f"\nposition: {position[0]}, {position[1]}, " +
                                 f"\ndirectional_field: {directional_field[0]}, {directional_field[1]}, " +
                                 f"\nwidth: {width}, " +
                                 f"\nheight: {height}, " +
                                 f"\nradius: {radius}" +
                                 f"\nnext_field: {next_field[0]}")
            circumference_fields.append(directional_field)
            directional_field = find_direction_field((direction + 2) % 6, directional_field, width, height)

    return circumference_fields


@njit(cache=True)
def _find_directional_fields(position, width, height, radius):
    directional_fields = List.empty_list(types.int64[:])

    for direction in range(6):
        direction_field = position.copy()
        for i in range(radius):
            direction_field = find_direction_field(direction, direction_field, width, height)
            if direction_field[0] < 0:
                break
        directional_fields.append(direction_field)

    return directional_fields
