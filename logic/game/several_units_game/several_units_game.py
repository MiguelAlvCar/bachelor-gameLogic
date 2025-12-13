from typing import Callable, Awaitable

from logic.game.comp_chasing_game.command import command
from logic.game.several_units_game.initialize import initialize
from logic.game.several_units_game.change_turn import change_turn
from logic.game.share.game_base import GameBase
from logic.game.several_units_game.generate_units.unit_generation_data import UnitGenerationData


class SeveralUnitsGame(GameBase):
    def __init__(self, on_finished: Callable[[float], Awaitable[None]], width: int, height: int, turn_number: int, hills_percentage: float, forests_percentage: float, cities_percentage: float,
                 blue_generation_data: UnitGenerationData, red_generation_data: UnitGenerationData):

        super().__init__(command, change_turn, on_finished)

        initialize(self, width, height, turn_number, hills_percentage, forests_percentage, cities_percentage,
                   blue_generation_data, red_generation_data)


