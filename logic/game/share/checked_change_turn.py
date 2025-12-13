from typing import Callable, Awaitable

from logic.game.share.game_base import GameBase
from logic.game.share.change_turn import change_turn
from logic.game.share.invalid_command_error import InvalidCommandError

async def checked_change_turn(game: GameBase, is_red_command: bool, on_finished: Callable[[float], Awaitable[None]]):
    if (game.is_red_turn and not is_red_command) or (not game.is_red_turn and is_red_command):
        raise InvalidCommandError(f"A command for {"red" if is_red_command else "blue"} units was receive during the "+
                                  f"{"blue" if is_red_command else "red"} turn")

    return await change_turn(game, on_finished)
