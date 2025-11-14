import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.map.map import Map


class GameBase:

    def __init__(self):
        self.map: Map = None

        self.blue_unit_types: npt.NDArray[np.int8] = None
        self.blue_unit_positions: npt.NDArray[np.int16] = None
        self.blue_unit_healths: npt.NDArray[np.float32] = None

        self.red_unit_types: npt.NDArray[np.int8] = None
        self.red_unit_positions: npt.NDArray[np.int16] = None
        self.red_unit_healths: npt.NDArray[np.float32] = None

        self.is_blue_win: bool = False
        self.is_red_win: bool = False
        self.is_tie: bool = False
        self.is_red_turn: bool = False
        self.turn_number: int = 0
        self.tie_turn_number = 100
