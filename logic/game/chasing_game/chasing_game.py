import numpy as np
import numpy.typing as npt
from typing import Callable

from logic.map.map import Map
from logic.game.share.random import get_random_not_overlapping_positions
from logic.game.share.invalid_command_error import InvalidCommandError
from logic.game.chasing_game.command_type import CommandType


def initialize (chasing_game: 'ChasingGame'):
    width: int = 10
    height: int = 8

    chasing_game.map = Map(width, height)

    number_of_blue_units = 1
    number_of_red_units = 1

    positions = get_random_not_overlapping_positions(width, height, number_of_blue_units + number_of_red_units)

    chasing_game.blue_unit_types = np.ones((number_of_blue_units), dtype=np.int8)
    chasing_game.blue_unit_positions = np.array([positions[0, :]], dtype=np.int16)
    chasing_game.map.position_blue_units[positions[0, 0], positions[0, 1]] = 0
    chasing_game.blue_unit_lifes = np.array([0.4], dtype=np.float32)

    chasing_game.red_unit_types = np.ones((number_of_red_units), dtype=np.int8)
    chasing_game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
    chasing_game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
    chasing_game.red_unit_lifes = np.array([1.], dtype=np.float32)

    chasing_game.is_red_turn = False


def command(chasing_game: 'ChasingGame', unit_index: int, command_index: CommandType, is_red_command: bool) -> tuple[npt.NDArray[np.int16], npt.NDArray[np.int16]]:
    if (chasing_game.is_red_turn and not is_red_command) or (not chasing_game.is_red_turn and is_red_command):
        raise InvalidCommandError(f"A command for {"red" if is_red_command else "blue"} units was receive during the "+
                                  f"{"blue" if is_red_command else "red"} turn")

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
        raise InvalidCommandError("Movement in contrary unit")

    position_own_units[unit_positions[unit_index][0], unit_positions[unit_index][1]] = -1
    position_own_units[target_field[0], target_field[1]] = unit_index
    unit_positions[unit_index] = target_field
    chasing_game.is_red_turn = not chasing_game.is_red_turn

    if is_red_command:
        edited_red_units = np.append(edited_red_units, unit_index)
    else:
        edited_blue_units = np.append(edited_blue_units, unit_index)

    return edited_red_units, edited_blue_units



class ChasingGame:

    map: Map

    blue_unit_types: npt.NDArray[np.int8]
    blue_unit_positions: npt.NDArray[np.int16]
    blue_unit_lifes: npt.NDArray[np.float32]

    red_unit_types: npt.NDArray[np.int8]
    red_unit_positions: npt.NDArray[np.int16]
    red_unit_lifes: npt.NDArray[np.float32]

    is_red_turn: bool

    command_fn: Callable

    def __init__(self, initialize = initialize, command = command):
        initialize(self)
        self.command_fn = command

    def command(self, unit_index, command_type, is_red_command):
        return self.command_fn(self, unit_index, command_type, is_red_command)



