import unittest
import numpy as np
import numpy.testing as npt

from logic.game.share.game_base import GameBase
from logic.map.map import Map
from logic.game.comp_chasing_game.comp_chasing_game import CompChasingGame
from logic.game.share.set_movement import set_movement
from logic.game.comp_chasing_game.exchange_position import exchange_positions
from logic.map.geometry.directions import Directions
from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.coordinates.axial_to_evenr import axial_to_evenr

def make_initialize_mock(
        red_positions = np.array([[1,1]]),
        blue_positions = np.array([[0,0],[2,0],[2, 1],[1, 2]])):

    def initialize_mock(game: 'GameBase'):
        width: int = 10
        height: int = 8

        game.map = Map(width, height)

        game.blue_unit_types = np.zeros(blue_positions.shape[0], dtype=np.int8)
        game.blue_unit_positions = blue_positions
        game.map.position_blue_units[blue_positions[:, 0], blue_positions[:, 1]] = np.arange(blue_positions.shape[0])
        game.blue_unit_healths = np.ones(blue_positions.shape[0], dtype=np.float32)
        game.blue_unit_organization = np.ones(blue_positions.shape[0], dtype=np.float32)
        game.blue_unit_movement = set_movement(game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)

        game.red_unit_types = np.zeros(red_positions.shape[0], dtype=np.int8)
        game.red_unit_positions = red_positions
        game.map.position_red_units[red_positions[:, 0], red_positions[:, 1]] = np.arange(red_positions.shape[0])
        game.red_unit_healths = np.ones(red_positions.shape[0], dtype=np.float32)
        game.red_unit_organization = np.ones(red_positions.shape[0], dtype=np.float32)
        game.red_unit_organization[0] = 0.21
        game.red_unit_movement = set_movement(game.red_unit_types, game.red_unit_positions, game.map.terrain_types)

        game.is_red_turn = False

    return initialize_mock


class TestRulesSeveralUnits(unittest.IsolatedAsyncioTestCase):

    async def test_exchange_positions(self):
        initialize_fn = make_initialize_mock(blue_positions = np.array([[2,0],[2, 1]]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        old_position1 = game.blue_unit_positions[0].copy()
        old_position2 = game.blue_unit_positions[1].copy()

        exchange_positions(0, 1, game.blue_unit_positions, game.map.position_blue_units)

        npt.assert_array_equal(old_position1, game.blue_unit_positions[1])
        npt.assert_array_equal(old_position2, game.blue_unit_positions[0])


    async def test_combat1(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0],[2,0],[2, 1],[1, 2]]), 8)
        )

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        old_position1 = game.red_unit_positions[0].copy()

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False,)

        npt.assert_array_equal(old_position1, game.red_unit_positions[0])


    async def test_combat2(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[2,1],[1, 2]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0],[2,0]]), 8)
        )
        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        old_position1 = game.red_unit_positions[0].copy()
        old_position2 = game.red_unit_positions[1].copy()

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(old_position1, game.red_unit_positions[1])
        npt.assert_array_equal(old_position2, game.red_unit_positions[0])


    async def test_combat3(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[1,2]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0],[2,0]]), 8)
        )
        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([2,1]))


    async def test_combat4(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0],[2,1]]), 8)
        )
        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        self.assertTrue(np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([2,0])) or
                        np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([1,2])) )


    async def test_combat5(self):
        left = False
        right = False
        i = 0

        while (not left or not right) and i < 16:
            i += 1

            initialize_fn = make_initialize_mock(
                red_positions = evenr_to_axial(np.array([[1,1],[1,2],[2,0]]), 8),
                blue_positions = evenr_to_axial(np.array([[0,0],[2,1]]), 8)
            )
            game = CompChasingGame(None, 8, 8, 0., 0., 0.)
            initialize_fn(game)

            await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

            if np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([2,0])):
                left = True
            elif np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([1,2])):
                right = True
            else:
                raise ValueError(f"Unexpected position: {game.red_unit_positions}")

        if not left or not right:
            raise ValueError("Both positions were not achieved: left: {left}; right: {right}")


    async def test_combat6(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[2,0],[2, 1],[1, 2]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0]]), 8)
        )

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        old_position1 = game.red_unit_positions[0].copy()
        old_position2 = game.red_unit_positions[2].copy()

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(old_position1, game.red_unit_positions[2])
        npt.assert_array_equal(old_position2, game.red_unit_positions[0])


    async def test_combat7(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[2, 1],[1, 2]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0]]), 8)
        )

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([2,0]))


    async def test_combat8(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[2,0],[2, 1]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0]]), 8)
        )

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([1, 2]))


    async def test_combat9(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,0]]), 8),
            blue_positions = evenr_to_axial(np.array([[2,0]]), 8)
        )

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.UP_LEFT, is_red_command=False)

        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([0, 0]))


    async def test_combat10(self):
        initialize_fn = make_initialize_mock(
            red_positions = evenr_to_axial(np.array([[1,1],[1,2]]), 8),
            blue_positions = evenr_to_axial(np.array([[0,0],[2,1],[2,0]]), 8)
        )
        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([1,2]))


    async def test_combat11(self):
        left = False
        right = False
        i = 0

        while (not left or not right) and i < 16:
            i += 1

            initialize_fn = make_initialize_mock(
                red_positions = evenr_to_axial(np.array([[1,1]]), 8),
                blue_positions = evenr_to_axial(np.array([[0,0],[2,1]]), 8)
            )
            game = CompChasingGame(None, 8, 8, 0., 0., 0.)
            initialize_fn(game)

            await game.command(unit_index=0, command_type=Directions.DOWN_RIGHT, is_red_command=False)

            if np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([2,0])):
                left = True
            elif np.array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([1,2])):
                right = True
            else:
                raise ValueError(f"Unexpected position: {game.red_unit_positions}")

        if not left or not right:
            raise ValueError("Both positions were not achieved: left: {left}; right: {right}")




