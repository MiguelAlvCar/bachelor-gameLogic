from logic.game.chasing_game.chasing_game_base import ChasingGameBase
from logic.game.chasing_game.command import command
from logic.game.chasing_game.initialize import initialize


class ChasingGame(ChasingGameBase):
    def __init__(self):
        super().__init__(initialize, command)
