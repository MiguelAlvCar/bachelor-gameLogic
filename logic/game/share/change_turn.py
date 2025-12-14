from typing import Callable, Awaitable

from logic.game.share.game_base import GameBase
from logic.game.share.reset_movement import reset_movement


async def change_turn(game: GameBase, on_finished: Callable[[float], Awaitable[None]]):
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
    game.turn_number = game.turn_number + 1
    if game.turn_number > game.total_number_turns:
        result = 0
        if on_finished:
            await on_finished(result)
        game.result = result

    return game.total_number_turns - game.turn_number
