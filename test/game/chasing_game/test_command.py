import unittest
import numpy as np
import numpy.testing as npt
import random
from typing import Callable, Awaitable

from logic.game.share.game_base import GameBase
from logic.map.map import Map
from logic.game.share.invalid_command_error import InvalidCommandError
from logic.map.geometry.directions import Directions
from logic.game.chasing_game.command import command
from logic.game.chasing_game.chasing_game import ChasingGame

def make_initialize_mock(positions_par, healths = np.array([1.0, 1.0])):
    def initialize_mock (chasing_game: 'GameBase'):
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
        is_on_winning_run["run"] = True
    return on_winning

def make_on_tie(is_on_tide_run: dict[str, bool]) -> Callable[[bool], Awaitable[None]]:
    async def on_tie(result: float) -> None:
        is_on_tide_run["run"] = True
    return on_tie

class TestCommand(unittest.IsolatedAsyncioTestCase):
    async def test_command_error1(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        with self.assertRaises(InvalidCommandError) as error:
            await game.command(unit_index=0, command_type=Directions.DOWN_LEFT, is_red_command=True)
        self.assertEqual(str(error.exception), "A command for red units was receive during the blue turn")

    async def test_command_error2(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        with self.assertRaises(InvalidCommandError) as error:
            await game.command(unit_index=1, command_type=Directions.DOWN_LEFT, is_red_command=False)
        self.assertEqual(str(error.exception), "The index of the unit '1' is higher or equal than the number of units '1'")

    async def test_command_quiet(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        await game.command(unit_index=0, command_type=Directions.QUIET, is_red_command=False)
        npt.assert_array_equal(game.blue_unit_positions, np.array([[0, 0]]))
        self.assertTrue(not game.is_red_turn)

    async def test_command_error4(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[0, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        with self.assertRaises(InvalidCommandError) as error:
            await game.command(unit_index=0, command_type=Directions.UP_LEFT, is_red_command=False)
        self.assertEqual(str(error.exception), "Movement outside of board")

    async def test_command_1(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)
        npt.assert_array_equal(game.blue_unit_positions, np.array([[0, 1]]))
        self.assertFalse(game.is_red_turn)

    async def test_several_commands(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        random_numbers = [random.randint(0, 6) for _ in range(15)]

        is_red_command = False
        for number in random_numbers:
            try:
                if is_red_command:
                    unit_positions = game.red_unit_positions
                else:
                    unit_positions = game.blue_unit_positions

                old_healths = game.blue_unit_healths.copy()
                old_position = unit_positions[0].copy()

                await game.command(unit_index=0, command_type=Directions(number), is_red_command=is_red_command)
                if Directions(number) != Directions.QUIET and old_healths[0] == game.blue_unit_healths[0]:
                    self.assertFalse(np.array_equal(old_position, unit_positions[0]))
            except InvalidCommandError as e:
                await game.command(unit_index=0, command_type=Directions.QUIET, is_red_command=is_red_command)

            await game.change_turn(is_red_command)

            is_red_command = not is_red_command

    async def test_combat1(self):
        initialize_fn = make_initialize_mock(np.array([[1, 2],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)
        old_blue_positions = game.blue_unit_positions.copy()
        old_red_positions = game.red_unit_positions.copy()

        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=False)

        np.testing.assert_array_equal(game.red_unit_positions, old_red_positions)
        np.testing.assert_array_equal(game.blue_unit_positions, old_blue_positions)

    async def test_combat2(self):
        initialize_fn = make_initialize_mock(np.array([[1, 2],[1, 1]]))
        game = ChasingGame(None)
        initialize_fn(game)

        edited_units = await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=False)

        np.testing.assert_array_equal(edited_units[0], np.array([0]))
        np.testing.assert_array_equal(edited_units[1], np.array([0]))

    async def test_win1(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[0, 1]]), np.array([0.1, 0.1]))
        is_on_winning_run = {}
        game = ChasingGame(make_on_winning(is_on_winning_run))
        initialize_fn(game)
        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)
        await game.change_turn(False)

        self.assertTrue(is_on_winning_run["run"])

        with self.assertRaises(InvalidCommandError) as error:
            await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=True)

        self.assertEqual(str(error.exception), "A command was receive after the end of the game")

    async def test_tie1(self):
        initialize_fn = make_initialize_mock(np.array([[0, 0],[0, 1]]), np.array([1., 1.]))
        is_on_tie_run = {}
        on_tide = make_on_tie(is_on_tie_run)
        game = ChasingGame(on_tide)
        initialize_fn(game)
        game.turn_number = game.tie_turn_number - 1
        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)
        await game.change_turn(False)

        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=True)
        await game.change_turn(True)

        self.assertTrue(game.result == 0.5)
        self.assertTrue(is_on_tie_run["run"])

        with self.assertRaises(InvalidCommandError) as error:
            await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertEqual(str(error.exception), "A command was receive after the end of the game")


