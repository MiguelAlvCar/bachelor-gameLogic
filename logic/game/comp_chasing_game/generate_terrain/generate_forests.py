import random
import numpy as np

from logic.map.terrain_type import TerrainType
from logic.map.map import Map
from logic.map.geometry.expand_area import expand_area
from logic.map.coordinates.get_playable_fields import get_playable_fields
from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.coordinates.valid_coords import valid_coords

def generate_forests(map: Map, forest_percentage: float):
    padding = 4

    even_padded_width = map.even_width + 2 * padding
    padded_height = map.height + 2 * padding

    weights = np.ones((padded_height, even_padded_width))

    forest_coords = set()

    playable_fields = get_playable_fields(padded_height, even_padded_width + padded_height // 2)

    while len(forest_coords) < (map.even_width * map.height * forest_percentage):
        forest_size = random.randint(1, 13)
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        forest_begin = np.unravel_index(flat_index, probs.shape)
        forest_begin = evenr_to_axial(np.array([forest_begin], dtype=np.int16), padded_height)[0]

        forest_area = expand_area(forest_size, forest_begin, playable_fields, 2.5)

        forest_area = forest_area - padding
        forest_area = forest_area[valid_coords(forest_area, map.playable_fields)]

        forest_coords.update({(f[0], f[1]) for f in forest_area})

        for f in forest_area:
            if map.terrain_types[f[0], f[1]] == TerrainType.HILL.value:
                map.terrain_types[f[0], f[1]] = TerrainType.FOREST_HILL.value
            else:
                map.terrain_types[f[0], f[1]] = TerrainType.FOREST.value
