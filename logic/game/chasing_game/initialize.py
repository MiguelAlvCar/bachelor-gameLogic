import numpy as np

from logic.map.map import Map
from logic.game.share.get_random_positions import get_random_not_overlapping_positions
from logic.game.share.game_base import GameBase
from logic.game.share.set_movement import set_movement
from logic.map.coordinates.evenr_to_axial import evenr_to_axial

def initialize(game: GameBase):
    width: int = 10
    height: int = 8

    game.map = Map(width, height)

    number_of_blue_units = 1
    number_of_red_units = 1

    positions = get_random_not_overlapping_positions(width, height, number_of_blue_units + number_of_red_units)
    positions = evenr_to_axial(positions, game.map.height)

    lifes = np.random.uniform(0.1, 1.0, size=(2,)).astype(np.float32)

    game.blue_unit_types = np.zeros((number_of_blue_units), dtype=np.int8)
    game.blue_unit_positions = np.array([positions[0, :]], dtype=np.int16)
    game.map.position_blue_units[positions[0, 0], positions[0, 1]] = 0
    game.blue_unit_healths = np.array([lifes[0]], dtype=np.float32)
    game.blue_unit_organization = np.ones((number_of_blue_units), dtype=np.float32)
    game.blue_unit_movement = set_movement(game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)

    game.red_unit_types = np.zeros((number_of_red_units), dtype=np.int8)
    game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
    game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
    game.red_unit_healths = np.array([lifes[1]], dtype=np.float32)
    game.red_unit_organization = np.ones((number_of_red_units), dtype=np.float32)
    game.red_unit_movement = set_movement(game.blue_unit_types, game.blue_unit_positions, game.map.terrain_types)

    game.total_number_turns = 200
