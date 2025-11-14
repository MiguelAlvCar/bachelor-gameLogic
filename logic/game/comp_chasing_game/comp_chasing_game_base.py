import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.map.map import Map
from logic.map.geometry.directions import Directions
from logic.game.share.game_base import GameBase


class CompChasingGameBase(GameBase):

    def __init__(self, initialize, command, width: int, height: int, hills_percentage: float, forests_percentage: float, cities_percentage: float):

        super().__init__()

        initialize(self, width, height, hills_percentage, forests_percentage, cities_percentage)

        self.command_fn = command

    async def command(self, unit_index: int, command_type: Directions, is_red_command: bool,
                      on_winning: Callable[[bool], Awaitable[None]], on_tide: Callable[[], Awaitable[None]]
                ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
        return await self.command_fn(self, unit_index, command_type, is_red_command, on_winning, on_tide)
