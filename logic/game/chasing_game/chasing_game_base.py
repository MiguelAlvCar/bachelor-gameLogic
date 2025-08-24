import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.map.map import Map
from logic.game.chasing_game.command_type import CommandType


class ChasingGameBase:

    map: Map

    blue_unit_types: npt.NDArray[np.int8]
    blue_unit_positions: npt.NDArray[np.int16]
    blue_unit_healths: npt.NDArray[np.float32]

    red_unit_types: npt.NDArray[np.int8]
    red_unit_positions: npt.NDArray[np.int16]
    red_unit_healths: npt.NDArray[np.float32]

    is_red_turn: bool
    _is_red_win: bool
    _is_blue_win: bool

    command_fn: Callable

    def __init__(self, initialize, command):
        self._is_blue_win = False
        self._is_red_win = False
        initialize(self)
        self.command_fn = command

    async def command(self, unit_index: int, command_type: CommandType, is_red_command: bool, on_winning: Callable[[bool], Awaitable[None]]
                ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
        return await self.command_fn(self, unit_index, command_type, is_red_command, on_winning)



