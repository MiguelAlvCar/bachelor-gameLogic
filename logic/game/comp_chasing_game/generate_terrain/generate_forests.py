import random
import numpy as np

from logic.map.terrain_type import TerrainType
from logic.map.map import Map
from logic.map.geometry.expand_area import expand_area

def generate_forests(map: Map, forest_percentage: float):
    padding = 4

    weights = np.ones((map.height + 2 * padding, map.width + 2 * padding))

    forest_coords = set()

    while len(forest_coords) < (map.width * map.height * forest_percentage):
        forest_size = random.randint(1, 13)
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        forest_begin = np.unravel_index(flat_index, probs.shape)

        forest_area = expand_area(forest_size, forest_begin, map.width + 2 * padding, map.height + 2 * padding, 2.5)

        forest_area = forest_area - padding
        forest_area = forest_area[
            (forest_area[:, 0] >= 0) &
            (forest_area[:, 0] < map.width) &
            (forest_area[:, 1] >= 0) &
            (forest_area[:, 1] < map.height)
        ]

        forest_coords.update({(f[0], f[1]) for f in forest_area})

        for f in forest_area:
            if map.terrain_types[f[1], f[0]] == TerrainType.HILL.value:
                map.terrain_types[f[1], f[0]] = TerrainType.FOREST_HILL.value
            else:
                map.terrain_types[f[1], f[0]] = TerrainType.FOREST.value
