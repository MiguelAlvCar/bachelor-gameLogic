import numpy as np
import numpy.typing as npt
from typing import Callable

from logic.map.find_next_fields import find_next_fields
from logic.map.find_direction_field import find_direction_field

class Map:
    _find_next_fields_fn: Callable
    _find_direction_field_fn: Callable

    def __init__(self, width: int, height: int, find_next_fields = find_next_fields, find_direction_field = find_direction_field):
        # First bool value: PLAIN
        self.field_types: npt.NDArray[np.bool_] = np.ones((height, width, 1), dtype=np.bool_)
        self.position_red_units: npt.NDArray[np.int16] = np.ones((height, width, 1), dtype=np.int16) * -1
        self.position_blue_units: npt.NDArray[np.int16] = np.ones((height, width, 1), dtype=np.int16) * -1
        self.width: int = width
        self.height: int = height

        self._find_next_fields_fn = find_next_fields
        self._find_direction_field_fn = find_direction_field

    def find_next_fields(self, position: npt.NDArray[np.int16]):
        return self._find_next_fields_fn(position, self.width, self.height)

    def find_direction_field(self, direction: int, position: npt.NDArray[np.int16]):
        return self._find_direction_field_fn(direction, position, self.width, self.height)





