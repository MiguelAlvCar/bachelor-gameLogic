import unittest
import numpy as np
import numpy.testing as npt
import random

from logic.game.chasing_game.chasing_game import ChasingGameBase
from logic.map.map import Map
from logic.game.share.invalid_command_error import InvalidCommandError
from logic.game.chasing_game.command_type import CommandType
from logic.game.chasing_game.command import command

def make_initialize_mock(positions_par):
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
        chasing_game.blue_unit_healths = np.array([0.4], dtype=np.float32)

        chasing_game.red_unit_types = np.ones((number_of_red_units), dtype=np.int8)
        chasing_game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
        chasing_game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
        chasing_game.red_unit_healths = np.array([1.], dtype=np.float32)

        chasing_game.is_red_turn = False
    return initialize_mock

class TestCommand(unittest.TestCase):
    def test_command_error1(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[1, 1]])), command=command)
        with self.assertRaises(InvalidCommandError) as error:
            game.command(unit_index=0, command_type=CommandType.DOWN_LEFT, is_red_command=True)
        self.assertEqual(str(error.exception), "A command for red units was receive during the blue turn")

    def test_command_error2(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[1, 1]])), command=command)
        with self.assertRaises(InvalidCommandError) as error:
            game.command(unit_index=1, command_type=CommandType.DOWN_LEFT, is_red_command=False)
        self.assertEqual(str(error.exception), "The index of the unit '1' is higher or equal than the number of units '1'")

    def test_command_quiet(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[1, 1]])), command=command)
        game.command(unit_index=0, command_type=CommandType.QUIET, is_red_command=False)
        npt.assert_array_equal(game.blue_unit_positions, np.array([[0, 0]]))
        self.assertTrue(game.is_red_turn)

    def test_command_error4(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[0, 1]])), command=command)
        with self.assertRaises(InvalidCommandError) as error:
            game.command(unit_index=0, command_type=CommandType.UP_LEFT, is_red_command=False)
        self.assertEqual(str(error.exception), "Movement outside of board")

    def test_command_1(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[1, 1]])), command=command)
        game.command(unit_index=0, command_type=CommandType.RIGHT, is_red_command=False)
        npt.assert_array_equal(game.blue_unit_positions, np.array([[0, 1]]))
        self.assertTrue(game.is_red_turn)

    def test_several_commands(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[0, 0],[1, 1]])), command=command)
        random_numbers = [random.randint(0, 6) for _ in range(20)]

        is_red_command = False
        for number in random_numbers:
            try:
                if is_red_command:
                    unit_positions = game.red_unit_positions
                else:
                    unit_positions = game.blue_unit_positions

                old_healths = game.blue_unit_healths.copy()
                old_position = unit_positions[0].copy()

                game.command(unit_index=0, command_type=CommandType(number), is_red_command=is_red_command)
                if CommandType(number) != CommandType.QUIET and old_healths[0] == game.blue_unit_healths[0]:
                    self.assertFalse(np.array_equal(old_position, unit_positions[0]))
            except InvalidCommandError as e:
                game.command(unit_index=0, command_type=CommandType.QUIET, is_red_command=is_red_command)

            is_red_command = not is_red_command

    def test_combat1(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[1, 2],[1, 1]])), command=command)
        old_blue_positions = game.blue_unit_positions.copy()
        old_red_positions = game.red_unit_positions.copy()

        game.command(unit_index=0, command_type=CommandType.LEFT, is_red_command=False)

        np.testing.assert_array_equal(game.red_unit_positions, old_red_positions)
        np.testing.assert_array_equal(game.blue_unit_positions, old_blue_positions)

    def test_combat2(self):
        game = ChasingGameBase(initialize=make_initialize_mock(np.array([[1, 2],[1, 1]])), command=command)

        edited_units = game.command(unit_index=0, command_type=CommandType.LEFT, is_red_command=False)

        np.testing.assert_array_equal(edited_units[0], np.array([0]))
        np.testing.assert_array_equal(edited_units[1], np.array([0]))
