import numpy.typing as npt
import numpy as np

from typing import Callable, Awaitable
from logic.game.chasing_game.chasing_game_base import ChasingGameBase


async def combat(game: ChasingGameBase, unit_index: int, enemy_unit_index: int, is_red_command: bool, on_winning: Callable[[bool], Awaitable[None]]
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
        await on_winning(is_red_command)
        if is_red_command:
            game.is_red_win = True
            return np.array([], dtype=np.int16), np.array([blue_index], dtype=np.int16)
        else:
            game.is_blue_win = True
            return np.array([red_index], dtype=np.int16), np.array([], dtype=np.int16)
    else:
        friend_healths[unit_index] -= 0.2
        if np.all(friend_healths < 0.001):
            await on_winning(not is_red_command)
            if is_red_command:
                game.is_blue_win = True
            else:
                game.is_red_win = True

    return np.array([red_index], dtype=np.int16), np.array([blue_index], dtype=np.int16)
