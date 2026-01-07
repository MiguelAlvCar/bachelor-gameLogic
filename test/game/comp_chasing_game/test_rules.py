import unittest
import numpy as np
import numpy.testing as npt

from logic.game.share.game_base import GameBase
from logic.map.map import Map
from logic.map.geometry.directions import Directions
from logic.game.comp_chasing_game.comp_chasing_game import CompChasingGame
from logic.game.share.set_movement import set_movement
from logic.game.share.unit_type import UnitType
from logic.map.terrain_type import TerrainType
from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.coordinates.axial_to_evenr import axial_to_evenr

def make_initialize_mock(
        positions_par,
        healths = np.array([1.0, 1.0]),
        organisation = np.array([1.0, 1.0]),
        unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]),
        terrain_type = TerrainType.PLAIN,
        terrain_location = np.array([0, 0])):

    def initialize_mock(game: 'GameBase'):
        width: int = 10
        height: int = 8

        game.map = Map(width, height)

        game.map.terrain_types[terrain_location[0], terrain_location[1]] = terrain_type.value

        positions = positions_par

        game.blue_unit_types = np.array([unit_types[0]], dtype=np.int8)
        game.blue_unit_positions = np.array([positions[0, :]], dtype=np.int16)
        game.map.position_blue_units[positions[0, 0], positions[0, 1]] = 0
        game.blue_unit_healths = np.array([healths[0]], dtype=np.float32)
        game.blue_unit_organization = np.array([organisation[0]], dtype=np.float32)
        game.blue_unit_movement = set_movement(game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)

        game.red_unit_types = np.array([unit_types[1]], dtype=np.int8)
        game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
        game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
        game.red_unit_healths = np.array([healths[1]], dtype=np.float32)
        game.red_unit_organization = np.array([organisation[1]], dtype=np.float32)
        game.red_unit_movement = set_movement(game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)

        game.is_red_turn = False

    return initialize_mock


class TestRules(unittest.IsolatedAsyncioTestCase):

    async def test_movement_cost(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            unit_types = np.array([UnitType.TANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.FOREST_HILL,
            terrain_location = evenr_to_axial(np.array([[0, 0]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=False)
        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=False)

        restmovement = game.blue_unit_movement[0]

        self.assertTrue(restmovement == -1)


    async def test_movement_bonus(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            unit_types = np.array([UnitType.TANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.HILL,
            terrain_location = evenr_to_axial(np.array([[0, 2]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)

        restmovement = game.blue_unit_movement[0]

        self.assertTrue(restmovement == 4)


    async def test_movement_bonus1(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            unit_types = np.array([UnitType.ANTITANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.HILL,
            terrain_location = evenr_to_axial(np.array([[0, 2]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)

        restmovement = game.blue_unit_movement[0]

        self.assertTrue(restmovement == 2)


    async def test_movement_bonus2(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            unit_types = np.array([UnitType.TANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.FOREST,
            terrain_location = evenr_to_axial(np.array([[0, 2]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)

        restmovement = game.blue_unit_movement[0]

        self.assertTrue(restmovement == 2)


    async def test_organisation(self):
        initial_orga = 0.5

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            organisation=np.array([initial_orga, 0.5]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)

        self.assertTrue(game.blue_unit_organization[0] == initial_orga)

        await game.change_turn(game.is_red_turn)

        self.assertTrue(game.blue_unit_organization[0] > initial_orga)


    async def test_combat1(self):

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(game.blue_unit_healths[0] < 1.)
        self.assertTrue(game.blue_unit_healths[0] < game.red_unit_healths[0])
        self.assertTrue(game.blue_unit_healths[0] > game.blue_unit_organization[0])
        self.assertTrue(game.red_unit_healths[0] > game.red_unit_organization[0])


    async def test_combat2(self):

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)
        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=True)

        self.assertTrue(game.red_unit_healths[0] < 1.)
        self.assertTrue(game.red_unit_healths[0] < game.blue_unit_healths[0])
        self.assertTrue(game.blue_unit_healths[0] > game.blue_unit_organization[0])
        self.assertTrue(game.red_unit_healths[0] > game.red_unit_organization[0])


    async def test_combat3(self):

        initialize_fn1 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.TANK.value]),
            terrain_type = TerrainType.FOREST,
            terrain_location = evenr_to_axial(np.array([[0, 1]]), 8)[0])

        game1 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn1(game1)

        await game1.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        initialize_fn2 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.TANK.value]),
            terrain_type = TerrainType.PLAIN,
            terrain_location = evenr_to_axial(np.array([[0, 1]]), 8)[0])

        game2 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn2(game2)

        await game2.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(game1.red_unit_healths[0] < game2.red_unit_healths[0])


    async def test_combat4(self):

        initialize_fn1 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.TANK.value]))

        game1 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn1(game1)

        await game1.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        initialize_fn2 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.ANTITANK.value, UnitType.TANK.value]))

        game2 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn2(game2)

        await game2.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(game1.red_unit_healths[0] > game2.red_unit_healths[0])


    async def test_combat5(self):

        initialize_fn1 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.TANK.value, UnitType.INFANTRY.value]),
            terrain_type = TerrainType.FOREST,
            terrain_location = evenr_to_axial(np.array([[0, 1]]), 8)[0])

        game1 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn1(game1)

        await game1.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        initialize_fn2 = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.TANK.value, UnitType.INFANTRY.value]),
            terrain_type = TerrainType.PLAIN,
            terrain_location = evenr_to_axial(np.array([[0, 1]]), 8)[0])

        game2 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn2(game2)

        await game2.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(game1.red_unit_healths[0] > game2.red_unit_healths[0])


    async def test_combat6(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            organisation = np.array([1.0, 0.21]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(game.red_unit_organization[0] < 0.2)
        npt.assert_array_equal(axial_to_evenr(game.red_unit_positions, 8)[0], np.array([0,2]))


    async def test_combat7(self):

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([0.3, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game1 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game1)

        await game1.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)


        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([1.0, 1.0]),
            organisation = np.array([1.0, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game2 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game2)

        await game2.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)


        self.assertTrue(game1.red_unit_healths[0] > game2.red_unit_healths[0])


    async def test_combat8(self):

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([0.5, 1.0]),
            organisation = np.array([0.5, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.change_turn(game.is_red_turn)
        await game.change_turn(game.is_red_turn)

        self.assertTrue(game.blue_unit_organization[0] == 0.5)


    async def test_combat9(self):

        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 0],[0, 1]]), 8),
            healths = np.array([0.3, 1.0]),
            organisation = np.array([0.3, 1.0]),
            unit_types = np.array([UnitType.INFANTRY.value, UnitType.INFANTRY.value]))

        game1 = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game1)

        await game1.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)


    async def test_occupied_terrain1(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[1, 1]]), 8),
            unit_types = np.array([UnitType.TANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.CITY,
            terrain_location = evenr_to_axial(np.array([[0, 3]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)

        self.assertTrue(tuple(evenr_to_axial(np.array([[0, 3]]), 8)[0]) in game.map.blue_occupied_fields)


    async def test_occupied_terrain2(self):
        initialize_fn = make_initialize_mock(
            evenr_to_axial(np.array([[0, 2],[0, 4]]), 8),
            unit_types = np.array([UnitType.TANK.value, UnitType.TANK.value]),
            terrain_type = TerrainType.CITY,
            terrain_location = evenr_to_axial(np.array([[0, 3]]), 8)[0])

        game = CompChasingGame(None, 8, 8, 0., 0., 0.)
        initialize_fn(game)

        await game.command(unit_index=0, command_type=Directions.RIGHT, is_red_command=False)
        await game.change_turn(game.is_red_turn)
        await game.change_turn(game.is_red_turn)
        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=False)
        await game.change_turn(game.is_red_turn)
        await game.command(unit_index=0, command_type=Directions.LEFT, is_red_command=True)

        self.assertTrue(not tuple(evenr_to_axial(np.array([[0, 3]]), 8)[0]) in game.map.blue_occupied_fields)
        self.assertTrue(tuple(evenr_to_axial(np.array([[0, 3]]), 8)[0]) in game.map.red_occupied_fields)
