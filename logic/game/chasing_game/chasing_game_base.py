import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.map.map import Map
from logic.game.chasing_game.command_type import CommandType


class ChasingGameBase:

    def __init__(self, initialize, command):
        self.map: Map = None

        self.blue_unit_types: npt.NDArray[np.int8] = None
        self.blue_unit_positions: npt.NDArray[np.int16] = None
        self.blue_unit_healths: npt.NDArray[np.float32] = None

        self.red_unit_types: npt.NDArray[np.int8] = None
        self.red_unit_positions: npt.NDArray[np.int16] = None
        self.red_unit_healths: npt.NDArray[np.float32] = None

        self.command_fn: Callable = None

        self.is_blue_win: bool = False
        self.is_red_win: bool = False
        self.is_tie: bool = False
        self.is_red_turn: bool = False
        self.turn_number: int = 0
        self.tie_turn_number = 100

        initialize(self)

        self.command_fn = command

    async def command(self, unit_index: int, command_type: CommandType, is_red_command: bool,
                      on_winning: Callable[[bool], Awaitable[None]], on_tide: Callable[[], Awaitable[None]]
                ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
        return await self.command_fn(self, unit_index, command_type, is_red_command, on_winning, on_tide)



