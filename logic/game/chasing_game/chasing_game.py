from typing import Callable, Awaitable

from logic.game.share.game_base import GameBase
from logic.game.chasing_game.command import command
from logic.game.chasing_game.initialize import initialize
from logic.game.share.checked_change_turn import checked_change_turn


class ChasingGame(GameBase):
    def __init__(self, on_finished: Callable[[float], Awaitable[None]]):
        super().__init__(command, checked_change_turn, on_finished)

        initialize(self)
