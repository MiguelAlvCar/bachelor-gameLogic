import numpy as np
import numpy.typing as npt

from logic.map.geometry.find_valid_circumference import find_valid_circumference
from logic.map.geometry.find_direction import find_direction
from logic.map.geometry.find_direction_field import find_direction_field
from logic.map.coordinates.get_playable_fields import get_playable_fields


class Map:

    def __init__(self, even_width: int, height: int, find_circumference = find_valid_circumference, find_direction_field = find_direction_field, find_direction = find_direction):
        self.height: int = height
        self.even_width: int = even_width
        self.axial_width: int = even_width + self.height // 2

        self.playable_fields: npt.NDArray[np.bool_] = get_playable_fields(self.height, self.axial_width)

        self.terrain_types: npt.NDArray[np.int16] = np.zeros((self.axial_width, self.height), dtype=np.int16)
        self.position_red_units: npt.NDArray[np.int16] = np.ones((self.axial_width, self.height), dtype=np.int16) * -1
        self.position_blue_units: npt.NDArray[np.int16] = np.ones((self.axial_width, self.height), dtype=np.int16) * -1
        self.red_occupied_fields: dict[tuple[int, int], None] = {}
        self.blue_occupied_fields: dict[tuple[int, int], None] = {}
        self.number_cities = 0

        self._find_circumference_fn = find_circumference
        self._find_direction_field_fn = find_direction_field
        self._find_direction_fn = find_direction


    def find_next_fields(self, position: npt.NDArray[np.int16]):
        return self._find_circumference_fn(position, self.playable_fields, 1)

    def find_direction_field(self, direction: int, position: npt.NDArray[np.int16]):
        return self._find_direction_field_fn(direction, position)

    def find_direction(self, origin: npt.NDArray[np.int16], target: npt.NDArray[np.int16]):
        return self._find_direction_fn(origin, target)
