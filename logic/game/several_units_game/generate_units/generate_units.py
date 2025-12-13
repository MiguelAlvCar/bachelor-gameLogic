import random
import numpy as np

from logic.game.share.game_base import GameBase
from logic.game.several_units_game.generate_units.generate_deployment_areas import generate_deployment_areas
from logic.game.share.unit_type import UnitType
from logic.game.several_units_game.generate_units.unit_generation_data import UnitGenerationData
from logic.game.share.set_movement import set_movement


def generate_units(game: GameBase,
        blue_generation_data: UnitGenerationData,
        red_generation_data: UnitGenerationData):

    type_numbers = np.arange(len(UnitType))
    areas = generate_deployment_areas(game.map)

    blue_area_view = areas[0].view([('x', areas[0].dtype), ('y', areas[0].dtype)])
    red_area_view = areas[1].view([('x', areas[1].dtype), ('y', areas[1].dtype)])

    blue_area = np.setdiff1d(blue_area_view, red_area_view).view(areas[0].dtype).reshape(-1, 2)
    red_area = np.setdiff1d(red_area_view, blue_area_view).view(areas[1].dtype).reshape(-1, 2)

    game.blue_unit_types, game.blue_unit_healths, game.blue_unit_organization, game.blue_unit_positions, game.blue_unit_movement = \
        _fill_unit_data(blue_generation_data, type_numbers, blue_area, game.map.position_blue_units, game.map.terrain_types)
    game.red_unit_types, game.red_unit_healths, game.red_unit_organization, game.red_unit_positions, game.red_unit_movement = \
        _fill_unit_data(red_generation_data, type_numbers, red_area, game.map.position_red_units, game.map.terrain_types)


def _fill_unit_data(generation_data: UnitGenerationData, type_numbers, area, position_units, terrain_types):
    if generation_data.is_fixed_unit_number:
        units_number = generation_data.units_number
    else:
        units_number = random.randint(generation_data.units_number - 2, generation_data.units_number + 2)

    if units_number < 1:
        units_number = 1

    if generation_data.unit_type_probs is None:
        probs = [0.8] + [0.2 / (len(UnitType) - 1)] * (len(UnitType) - 1)
    else:
        probs = [generation_data.unit_type_probs[k] for k in sorted(generation_data.unit_type_probs.keys())]

    unit_types = np.random.choice(type_numbers, size=units_number, p=probs, replace=True)
    unit_healths = np.ones([units_number], dtype=np.float32)
    unit_organization = np.ones([units_number], dtype=np.float32)

    location_indices = np.random.choice(area.shape[0], size=units_number, replace=False)
    unit_positions = area[location_indices, :]
    position_units[unit_positions[:, 0], unit_positions[:, 1]] = np.arange(units_number)

    unit_movement = set_movement(unit_types, unit_positions, terrain_types)

    return unit_types, unit_healths, unit_organization, unit_positions, unit_movement
