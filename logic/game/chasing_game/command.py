import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable

from logic.game.share.invalid_command_error import InvalidCommandError
from logic.game.chasing_game.command_type import CommandType
from logic.game.chasing_game.chasing_game_base import ChasingGameBase
from logic.game.chasing_game.combat import combat

async def command(chasing_game: ChasingGameBase, unit_index: int, command_index: CommandType, is_red_command: bool,
            on_winning: Callable[[bool], Awaitable[None]]
            ) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
    if (chasing_game.is_red_turn and not is_red_command) or (not chasing_game.is_red_turn and is_red_command):
        raise InvalidCommandError(f"A command for {"red" if is_red_command else "blue"} units was receive during the "+
                                  f"{"blue" if is_red_command else "red"} turn")
    if (chasing_game._is_red_win or chasing_game._is_blue_win):
        raise InvalidCommandError("A command was receive after the win")

    if is_red_command:
        unit_positions = chasing_game.red_unit_positions
        position_contrary_units = chasing_game.map.position_blue_units
        position_own_units = chasing_game.map.position_red_units
    else:
        unit_positions = chasing_game.blue_unit_positions
        position_contrary_units = chasing_game.map.position_red_units
        position_own_units = chasing_game.map.position_blue_units

    if unit_positions.shape[0] <= unit_index:
        raise InvalidCommandError(f"The index of the unit '{unit_index}' is higher or equal than the number of units '{unit_positions.shape[0]}'")

    edited_red_units = np.array([], dtype=np.int16)
    edited_blue_units = np.array([], dtype=np.int16)
    if command_index == CommandType.QUIET:
        chasing_game.is_red_turn = not chasing_game.is_red_turn
        return edited_red_units, edited_blue_units

    target_field = chasing_game.map.find_direction_field(command_index.value, unit_positions[unit_index])

    if target_field[0] == -1:
        raise InvalidCommandError("Movement outside of board")

    if position_contrary_units[target_field[0], target_field[1]] != -1:
        edited_red_units, edited_blue_units = await combat(chasing_game,
                                                     unit_index,
                                                     position_contrary_units[target_field[0], target_field[1]][0],
                                                     is_red_command,
                                                     on_winning)
    else:
        position_own_units[unit_positions[unit_index][0], unit_positions[unit_index][1]] = -1
        position_own_units[target_field[0], target_field[1]] = unit_index
        unit_positions[unit_index] = target_field

        if is_red_command:
            edited_red_units = np.append(edited_red_units, unit_index)
        else:
            edited_blue_units = np.append(edited_blue_units, unit_index)

    chasing_game.is_red_turn = not chasing_game.is_red_turn
    return edited_red_units, edited_blue_units
