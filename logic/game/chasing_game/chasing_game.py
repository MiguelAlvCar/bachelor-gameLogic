import numpy as np
import numpy.typing as npt

from logic.map.map import Map
from logic.game.share.random import get_random_not_overlapping_positions


class ChasingGame:
    def __init__(self):
        width: int = 10
        height: int = 8

        self.map: Map = Map(width, height)

        number_of_blue_units = 1
        number_of_red_units = 1

        positions = get_random_not_overlapping_positions(width, height, number_of_blue_units + number_of_red_units)

        self.blue_unit_types: npt.NDArray[np.int8] = np.ones((number_of_blue_units), dtype=np.int8)
        self.blue_unit_positions: npt.NDArray[np.int16] = np.array([positions[0, :]], dtype=np.int16)
        self.blue_unit_lifes: npt.NDArray[np.float32] = np.array([0.4], dtype=np.float32)

        self.red_unit_types: npt.NDArray[np.int8] = np.ones((number_of_red_units), dtype=np.int8)
        self.red_unit_positions: npt.NDArray[np.int16] = np.array([positions[1, :]], dtype=np.int16)
        self.red_unit_lifes: npt.NDArray[np.float32] = np.array([1.], dtype=np.float32)
