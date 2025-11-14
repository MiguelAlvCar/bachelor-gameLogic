import math
from numba import njit
from numba.typed import List
import numpy as np

@njit(cache=True)
def find_hex_line(axial_origin, axial_end):
    distance = max(abs(axial_origin[0] - axial_end[0]),
                   abs(axial_origin[1] - axial_end[1]),
                   abs(axial_end[0] + axial_end[1] - axial_origin[0] - axial_origin[1]))
    results = List.empty_list(np.int64[:])
    for i in range(distance + 1):
        interval = 0 if distance == 0 else i / distance
        results.append(_cube_round(_cube_lerp(axial_origin, axial_end, interval)))
    return results

@njit(cache=True)
def _cube_round(coor):
    rq, rr = round(coor[0]), round(coor[1])
    rs = -rq - rr
    dq, dr, ds = abs(rq - coor[0]), abs(rr - coor[1]), abs(rs + coor[0] + coor[1])
    if dq > dr and dq > ds:
        rq = -rr - rs
    elif dr > ds:
        rr = -rq - rs
    return np.array([rq, rr])

@njit(cache=True)
def _cube_lerp(origin, end, interval):
    return np.array([origin[0] + (end[0] - origin[0]) * interval,
            origin[1] + (end[1] - origin[1]) * interval])
