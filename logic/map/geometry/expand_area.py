import random
import numpy as np
import numpy.typing as npt
from numba import njit
from numba import types
from numba.typed import Dict

from logic.map.geometry.find_valid_circumference import find_valid_circumference


# not compiled with numba, bacause random.choices is used
def expand_area(area_size, area_start: npt.NDArray[np.int64], playable_fields, rate):
    area_coords = Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=types.boolean,
    )

    adjacent_coords = Dict.empty(
        key_type=types.UniTuple(types.float64, 2),
        value_type=types.float32,
    )

    _add_adjacent_coords(area_coords, adjacent_coords, area_start, playable_fields, rate)

    for _ in range(0, area_size - 1):
        keys = list(adjacent_coords.keys())
        values = np.array(list(adjacent_coords.values()), dtype=float)
        probs = values / values.sum()
        deployment_field = random.choices(keys, weights=probs)[0]
        deployment_field = np.array(deployment_field, dtype=np.int64)

        _add_adjacent_coords(area_coords, adjacent_coords, deployment_field, playable_fields, rate)

    return _get_keys_as_array(area_coords)

#@njit(cache=True)
def _add_adjacent_coords(area_coords, adjacent_coords, deployment_field, playable_fields, rate):
    next_fields = find_valid_circumference(deployment_field, playable_fields, 1)

    deployment_field = (deployment_field[0].item(), deployment_field[1].item())
    area_coords[deployment_field] = True

    if deployment_field in adjacent_coords:
        del adjacent_coords[deployment_field]

    for f in next_fields:
        t = (f[0], f[1])
        if t in area_coords:
            continue

        if t in adjacent_coords:
            adjacent_coords[t] *= rate
        else:
            adjacent_coords[t] = 1

@njit(cache=True)
def _get_keys_as_array(d):
    size = len(d)
    arr = np.empty((size,2), dtype=np.int64)

    i = 0
    for key in d:
        arr[i] = key
        i += 1

    return arr

