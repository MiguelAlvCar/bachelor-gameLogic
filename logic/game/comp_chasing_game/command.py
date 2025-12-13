import numpy as np
import numpy.typing as npt
from typing import Callable, Awaitable, List

from logic.game.share.invalid_command_error import InvalidCommandError
from logic.map.geometry.directions import Directions
from logic.game.share.game_base import GameBase
from logic.game.comp_chasing_game.combat import combat
from logic.game.comp_chasing_game.rules.movement_cost import movement_cost
from logic.game.comp_chasing_game.change_position import change_position
from logic.game.comp_chasing_game.rules.general_rules import limit_organisation_attack

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
        own_organisation = game.red_unit_organization[unit_index]
    else:
        unit_positions = game.blue_unit_positions
        position_contrary_units = game.map.position_red_units
        position_own_units = game.map.position_blue_units
        unit_movement = game.blue_unit_movement
        own_organisation = game.blue_unit_organization[unit_index]

    if unit_positions.shape[0] <= unit_index:
        raise InvalidCommandError(f"The index of the unit '{unit_index}' is higher or equal than the number of units '{unit_positions.shape[0]}'")
    if unit_movement[unit_index] <= 0:
        raise InvalidCommandError(f"The unit '{unit_index}' has no movement points left")

    friend_ocupied_terrains: List[tuple[int, int]] = []
    enemy_ocupied_terrains: List[tuple[int, int]] = []

    edited_red_units = np.array([], dtype=np.int16)
    edited_blue_units = np.array([], dtype=np.int16)
    if command_index == Directions.QUIET:
        unit_movement[unit_index] = 0
        return edited_red_units, edited_blue_units, np.empty(), np.empty()

    target_field = game.map.find_direction_field(command_index.value, unit_positions[unit_index])

    if target_field[0] == -1:
        raise InvalidCommandError("Movement outside of board.")

    if position_contrary_units[target_field[0], target_field[1]] != -1:
        if is_red_command:
            own_healths = game.red_unit_healths[unit_index]
        else:
            own_healths = game.blue_unit_healths[unit_index]

        if own_organisation < limit_organisation_attack * own_healths:
            raise InvalidCommandError("Combat initiated with low organisation.")
        edited_red_units, edited_blue_units = await combat(game,
                                                     unit_index,
                                                     position_contrary_units[target_field[0], target_field[1]].item(),
                                                     is_red_command,
                                                     command_index,
                                                     friend_ocupied_terrains,
                                                     enemy_ocupied_terrains,
                                                     on_finished)
        unit_movement[unit_index] = 0
    else:
        change_position(unit_index, unit_positions, position_own_units, target_field,
                        friend_ocupied_terrains, game.map.terrain_types)

        if is_red_command:
            edited_red_units = np.append(edited_red_units, unit_index)
        else:
            edited_blue_units = np.append(edited_blue_units, unit_index)

        terrain_type = game.map.terrain_types[target_field[0], target_field[1]]
        unit_movement[unit_index] -= movement_cost[terrain_type.item()]

    if is_red_command:
        has_new_red_ocupied = len(friend_ocupied_terrains) > 0
        has_new_blue_ocupied = len(enemy_ocupied_terrains) > 0
        friend_ocupied_fields = game.map.red_occupied_fields
        enemy_ocupied_fields = game.map.blue_occupied_fields
    else:
        has_new_red_ocupied = len(enemy_ocupied_terrains) > 0
        has_new_blue_ocupied = len(friend_ocupied_terrains) > 0
        friend_ocupied_fields = game.map.blue_occupied_fields
        enemy_ocupied_fields = game.map.red_occupied_fields

    for ocupied_terrain in friend_ocupied_terrains:
        friend_ocupied_fields[ocupied_terrain] = None
        enemy_ocupied_fields.pop(ocupied_terrain, None)
    for ocupied_terrain in enemy_ocupied_terrains:
        enemy_ocupied_fields[ocupied_terrain] = None
        friend_ocupied_fields.pop(ocupied_terrain, None)

    return edited_red_units, edited_blue_units, has_new_red_ocupied, has_new_blue_ocupied

