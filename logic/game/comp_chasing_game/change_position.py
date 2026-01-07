from logic.map.terrain_type import TerrainType
from typing import List

def change_position(unit_index, unit_positions, map_positions, target_field,
                    occupied_terrains: List[tuple[int, int]], terrain_types):
    old_position = unit_positions[unit_index]
    map_positions[old_position[0], old_position[1]] = -1
    map_positions[target_field[0], target_field[1]] = unit_index
    unit_positions[unit_index] = target_field

    terrain_type = terrain_types[target_field[0], target_field[1]]
    if terrain_type == TerrainType.CITY.value or terrain_type == TerrainType.HILL_CITY.value:
        occupied_terrains.append(tuple(target_field))
