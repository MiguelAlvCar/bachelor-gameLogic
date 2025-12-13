import numpy.typing as npt
import numpy as np

from typing import Callable, Awaitable
from logic.game.share.game_base import GameBase


async def combat(game: GameBase, unit_index: int, enemy_unit_index: int, is_red_command: bool,
                 on_finished: Callable[[float], Awaitable[None]]
           ) -> Awaitable[tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]]:
    if is_red_command:
        enemy_healths = game.blue_unit_healths
        friend_healths = game.red_unit_healths
        red_index = unit_index
        blue_index = enemy_unit_index
    else:
        enemy_healths = game.red_unit_healths
        friend_healths = game.blue_unit_healths
        red_index = enemy_unit_index
        blue_index = unit_index

    enemy_healths[enemy_unit_index] -= 0.2
    if np.all(enemy_healths < 0.001):
        result = 1 if is_red_command else 0
        if on_finished:
            await on_finished(result)
        game.result = result
    else:
        friend_healths[unit_index] -= 0.2
        if np.all(friend_healths < 0.001):
            result = 0 if is_red_command else 1
            if on_finished:
                await on_finished(result)
            game.result = result

    return np.array([red_index], dtype=np.int16), np.array([blue_index], dtype=np.int16)
