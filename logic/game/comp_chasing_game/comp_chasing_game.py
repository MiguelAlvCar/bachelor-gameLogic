from typing import Callable, Awaitable

from logic.game.comp_chasing_game.command import command
from logic.game.comp_chasing_game.initialize import initialize
from logic.game.share.checked_change_turn import checked_change_turn
from logic.game.share.game_base import GameBase


class CompChasingGame(GameBase):
    def __init__(self, on_finished: Callable[[float], Awaitable[None]], width: int, height: int, hills_percentage: float, forests_percentage: float, cities_percentage: float):
        super().__init__(command, checked_change_turn, on_finished)

        initialize(self, width, height, hills_percentage, forests_percentage, cities_percentage)
