from logic.game.chasing_game.chasing_game_base import ChasingGameBase
import numpy.typing as npt
import numpy as np


def combat(game: ChasingGameBase, unit_index: int, enemy_unit_index: int, is_red_command: bool) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
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
    friend_healths[unit_index] -= 0.2

    return np.array([red_index], dtype=np.int16), np.array([blue_index], dtype=np.int16)
