import numpy as np

from logic.game.comp_chasing_game.generate_terrain.generate_terrain import generate_terrain
from logic.map.map import Map
from logic.game.share.get_random_positions import get_random_not_overlapping_positions
from logic.game.chasing_game.chasing_game_base import ChasingGameBase
from logic.game.share.unit_type import UnitType


def initialize(chasing_game: ChasingGameBase, width: int, height: int, hills_percentage: float, forests_percentage: float, cities_percentage: float):

    chasing_game.map = Map(width, height)

    number_of_blue_units = 1
    number_of_red_units = 1
    min_value = min(e.value for e in UnitType)
    max_value = max(e.value for e in UnitType)
    unit_types = np.random.randint(min_value, max_value + 1, size=2)

    positions = get_random_not_overlapping_positions(width, height, number_of_blue_units + number_of_red_units)

    lifes = np.random.uniform(0.1, 1.0, size=(2,)).astype(np.float32)

    chasing_game.blue_unit_types = np.array([unit_types[0]], dtype=np.int8)
    chasing_game.blue_unit_positions = np.array([positions[0, :]], dtype=np.int16)
    chasing_game.map.position_blue_units[positions[0, 0], positions[0, 1]] = 0
    chasing_game.blue_unit_healths = np.array([lifes[0]], dtype=np.float32)

    chasing_game.red_unit_types = np.array([unit_types[1]], dtype=np.int8)
    chasing_game.red_unit_positions = np.array([positions[1, :]], dtype=np.int16)
    chasing_game.map.position_red_units[positions[1, 0], positions[1, 1]] = 0
    chasing_game.red_unit_healths = np.array([lifes[1]], dtype=np.float32)

    generate_terrain(chasing_game.map, hills_percentage, forests_percentage, cities_percentage)
