from logic.game.comp_chasing_game.generate_terrain.generate_terrain import generate_terrain
from logic.game.several_units_game.generate_units.generate_units import generate_units
from logic.map.map import Map
from logic.game.share.game_base import GameBase
from logic.game.several_units_game.generate_units.unit_generation_data import UnitGenerationData
from logic.map.terrain_type import TerrainType


def initialize(game: GameBase, width: int, height: int, remaining_turns: int, hills_percentage: float, forests_percentage: float, cities_percentage: float,
               blue_generation_data: UnitGenerationData, red_generation_data: UnitGenerationData):

    game.map = Map(width, height)

    generate_terrain(game.map, hills_percentage, forests_percentage, cities_percentage)

    generate_units(game, blue_generation_data, red_generation_data)

    game.total_number_turns = remaining_turns

    for position in game.blue_unit_positions:
        terrain_type = game.map.terrain_types[position[0], position[1]]
        if terrain_type == TerrainType.CITY.value or terrain_type == TerrainType.HILL_CITY.value:
            game.map.blue_occupied_fields[tuple(position)] = None
    for position in game.red_unit_positions:
        terrain_type = game.map.terrain_types[position[0], position[1]]
        if terrain_type == TerrainType.CITY.value or terrain_type == TerrainType.HILL_CITY.value:
            game.map.red_occupied_fields[tuple(position)] = None
