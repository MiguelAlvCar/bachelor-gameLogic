from typing import Callable, Awaitable

from logic.game.share.game_base import GameBase
from logic.game.share.reset_movement import reset_movement
from logic.game.share.invalid_command_error import InvalidCommandError


async def change_turn(game: GameBase, is_red_command: bool, on_finished: Callable[[float], Awaitable[None]]):

    if (game.is_red_turn and not is_red_command) or (not game.is_red_turn and is_red_command):
        raise InvalidCommandError(f"A command for {"red" if is_red_command else "blue"} units was receive during the " +
                                  f"{"blue" if is_red_command else "red"} turn")

    if game.is_red_turn:
        reset_movement(game.blue_unit_movement, game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)
        game.blue_unit_organization = game.blue_unit_organization + 0.06
        mask = game.blue_unit_organization > game.blue_unit_healths
        game.blue_unit_organization[mask] = game.blue_unit_healths[mask]
    else:
        reset_movement(game.red_unit_movement, game.red_unit_types, game.red_unit_positions, game.map.terrain_types)
        game.red_unit_organization = game.red_unit_organization + 0.06
        mask = game.red_unit_organization > game.red_unit_healths
        game.red_unit_organization[mask] = game.red_unit_healths[mask]

    game.is_red_turn = not game.is_red_turn

    relativ_diff = (len(game.map.red_occupied_fields) - len(game.map.blue_occupied_fields)) / game.map.number_cities
    abs_relativ_diff =  abs(relativ_diff)

    turn_sum = 1
    if game.map.number_cities == 1:
        turn_sum += abs_relativ_diff
    else:
        turn_sum += abs_relativ_diff * 2
        if abs_relativ_diff > 0.5:
            turn_sum += (abs_relativ_diff - 0.5) * 6

    game.turn_number += turn_sum

    if game.turn_number > game.number_turns:
        result = (relativ_diff / 2) + 0.5
        if on_finished:
            await on_finished(result)
        game.result = result

    return (game.number_turns - game.turn_number) // turn_sum
