from logic.game.chasing_game.command import command
from logic.game.comp_chasing_game.initialize import initialize
from logic.game.comp_chasing_game.comp_chasing_game_base import CompChasingGameBase


class CompChasingGame(CompChasingGameBase):
    def __init__(self, width: int, height: int, hills_percentage: float, forest_percentage: float, cities_percentage: float):
        super().__init__(initialize, command, width, height, hills_percentage, forest_percentage, cities_percentage)
