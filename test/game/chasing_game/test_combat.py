import unittest
import numpy as np
from typing import Callable, Awaitable

from logic.game.chasing_game.chasing_game import ChasingGameBase
from logic.map.map import Map
from logic.game.chasing_game.combat import combat

def make_initialize_mock(healths, positions_par):
    def initialize_mock (chasing_game: 'ChasingGameBase'):
        width: int = 10
        height: int = 8

        chasing_game.map = Map(width, height)

        number_of_blue_units = 1
        number_of_red_units = 1

        positions = positions_par

        chasing_game.blue_unit_types = np.ones((number_of_blue_units), dtype=np.int8)
        chasing_game.blue_unit_positions = np.array([positions[0, :]], dtype=np.int16)
        chasing_game.map.position_blue_units[positions[0, 0], positions[0, 1]] = 0
        chasing_game.blue_unit_healths = np.array([healths[0]], dtype=np.float32)

        chasing_game.red_unit_types = np.ones((number_of_red_units), dtype=np.int8)
        chasing_game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
        chasing_game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
        chasing_game.red_unit_healths = np.array([healths[1]], dtype=np.float32)

        chasing_game.is_red_turn = False
    return initialize_mock

def make_on_winning(is_on_winning_run: dict[str, bool]) -> Callable[[bool], Awaitable[None]]:
    async def on_winning(is_red_winner: bool) -> None:
        is_on_winning_run["value"] = True
    return on_winning

class TestCombat(unittest.IsolatedAsyncioTestCase):
    async def test_combat(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([0.4, 1.0]), np.array([[0, 0],[1, 1]])), command=None)
        await combat(game, 0, 0, False, None)
        self.assertAlmostEqual(game.blue_unit_healths[0], 0.2)
        self.assertAlmostEqual(game.red_unit_healths[0], 0.8)

    async def test_win(self):
        is_on_winning_run = {"value": False}
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([1.0, 0.1]), np.array([[0, 0],[1, 1]])), command=None,)
        await combat(game, 0, 0, False, make_on_winning(is_on_winning_run))
        self.assertAlmostEqual(game.blue_unit_healths[0], 1.0)
        self.assertTrue(game.red_unit_healths[0] < 0.0)
        self.assertTrue(is_on_winning_run["value"])

