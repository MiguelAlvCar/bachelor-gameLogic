import numpy.typing as npt
import numpy as np

from logic.map.geometry.find_valid_circumference import find_valid_circumference


def make_get_neighbors(map_mask: npt.NDArray[np.bool_]):

    def get_neighbors(origin):
        candidates = find_valid_circumference(origin, map_mask, 1)
        return candidates

    return get_neighbors
