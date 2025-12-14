import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.map.map import Map
from logic.map.geometry.directions import Directions


class GameBase:

    def __init__(self, command, change_turn, on_finished: Callable[[float], Awaitable[None]]):
        self.map: Map = None

        self.blue_unit_types: npt.NDArray[np.int8] = None
        self.blue_unit_positions: npt.NDArray[np.int16] = None
        self.blue_unit_healths: npt.NDArray[np.float32] = None
        self.blue_unit_organization: npt.NDArray[np.float32] = None
        self.blue_unit_movement: npt.NDArray[np.int8] = None

        self.red_unit_types: npt.NDArray[np.int8] = None
        self.red_unit_positions: npt.NDArray[np.int16] = None
        self.red_unit_healths: npt.NDArray[np.float32] = None
        self.red_unit_organization: npt.NDArray[np.float32] = None
        self.red_unit_movement: npt.NDArray[np.int8] = None

        self.result: float | None = None
        self.is_red_turn: bool = False
        self.turn_number: int = 0

        self.command_fn: Callable = command
        self.change_turn_fn: Callable = change_turn
        self.on_finished: Callable[[float], Awaitable[None]] = on_finished

        self.total_number_turns: int = 0

    async def command(self, unit_index: int, command_type: Directions, is_red_command: bool,
                ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
        return await self.command_fn(self, unit_index, command_type, is_red_command, self.on_finished)

    async def change_turn(self, is_red_command: bool) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
        remaining_turns = await self.change_turn_fn(self, is_red_command, self.on_finished)
        return remaining_turns
