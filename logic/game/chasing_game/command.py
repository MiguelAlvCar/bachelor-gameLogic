import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.game.share.invalid_command_error import InvalidCommandError
from logic.map.geometry.directions import Directions
from logic.game.share.game_base import GameBase
from logic.game.chasing_game.combat import combat

async def command(game: GameBase, unit_index: int, command_index: Directions, is_red_command: bool,
            on_finished: Callable[[float], Awaitable[None]]
            ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
    if (game.is_red_turn and not is_red_command) or (not game.is_red_turn and is_red_command):
        raise InvalidCommandError(f"A command for {"red" if is_red_command else "blue"} units was receive during the "+
                                  f"{"blue" if is_red_command else "red"} turn")
    if game.result != None:
        raise InvalidCommandError("A command was receive after the end of the game")

    if is_red_command:
        unit_positions = game.red_unit_positions
        position_contrary_units = game.map.position_blue_units
        position_own_units = game.map.position_red_units
        unit_movement = game.red_unit_movement
    else:
        unit_positions = game.blue_unit_positions
        position_contrary_units = game.map.position_red_units
        position_own_units = game.map.position_blue_units
        unit_movement = game.blue_unit_movement

    if unit_positions.shape[0] <= unit_index:
        raise InvalidCommandError(f"The index of the unit '{unit_index}' is higher or equal than the number of units '{unit_positions.shape[0]}'")
    if unit_movement[unit_index] <= 0:
        raise InvalidCommandError(f"The unit '{unit_index}' has no movement points left")

    edited_red_units = np.array([], dtype=np.int16)
    edited_blue_units = np.array([], dtype=np.int16)
    if command_index == Directions.QUIET:
        unit_movement[unit_index] = 0
        return edited_red_units, edited_blue_units, False, False

    target_field = game.map.find_direction_field(command_index.value, unit_positions[unit_index])

    if target_field[0] == -1:
        raise InvalidCommandError("Movement outside of board")

    if position_contrary_units[target_field[0], target_field[1]] != -1:
        edited_red_units, edited_blue_units = await combat(game,
                                                     unit_index,
                                                     position_contrary_units[target_field[0], target_field[1]],
                                                     is_red_command,
                                                     on_finished)
    else:
        old_position = unit_positions[unit_index]
        position_own_units[old_position[0], old_position[1]] = -1
        position_own_units[target_field[0], target_field[1]] = unit_index
        unit_positions[unit_index] = target_field

        if is_red_command:
            edited_red_units = np.append(edited_red_units, unit_index)
        else:
            edited_blue_units = np.append(edited_blue_units, unit_index)

    unit_movement[unit_index] -= 1

    return edited_red_units, edited_blue_units, False, False

