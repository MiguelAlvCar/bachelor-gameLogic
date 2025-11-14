import random
import numpy as np

from logic.map.field_type import FieldType
from logic.map.map import Map
from collections import defaultdict

def generate_forests(map: Map, forest_percentage: float):
    padding = 4

    weights = np.ones((map.height + 2 * padding, map.width + 2 * padding))

    forest_coords = set()

    while len(forest_coords) < (map.width * map.height * forest_percentage):
        forest_size = random.randint(1, 17)
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        forest_begin = np.unravel_index(flat_index, probs.shape)

        adjacent_forest_coords = defaultdict(float)

        next_fields = map.find_next_fields(np.array(forest_begin))
        next_fields = next_fields[(next_fields[:, 0] >= 0)]
        forest_begin = forest_begin[0] - padding, forest_begin[1] - padding
        if (forest_begin[0] >= 0) and (forest_begin[1] >= 0) & (forest_begin[0] < map.height) & (forest_begin[1] < map.width):
            if map.field_types[forest_begin[0], forest_begin[1]] == FieldType.HILL.value:
                map.field_types[forest_begin[0], forest_begin[1]] = FieldType.FOREST_HILL.value
            else:
                map.field_types[forest_begin[0], forest_begin[1]] = FieldType.FOREST.value
            forest_coords.add(tuple(forest_begin))
        for f in next_fields:
            adjacent_forest_coords[tuple(f)] += 1.0

        for _ in range(1, forest_size):
            keys = list(adjacent_forest_coords.keys())
            values = np.array(list(adjacent_forest_coords.values()), dtype=float)
            probs = values / values.sum()
            forest_field = random.choices(keys, weights=probs, k=1)[0]

            next_fields = map.find_next_fields(np.array(forest_field))
            next_fields = next_fields[(next_fields[:, 0] >= 0)]
            forest_field = forest_field[0] - padding, forest_field[1] - padding
            if (forest_field[0] >= 0) and (forest_field[1] >= 0) & (forest_field[0] < map.height) & (forest_field[1] < map.width):
                if map.field_types[forest_field[0], forest_field[1]] == FieldType.HILL.value:
                    map.field_types[forest_field[0], forest_field[1]] = FieldType.FOREST_HILL.value
                else:
                    map.field_types[forest_field[0], forest_field[1]] = FieldType.FOREST.value
                forest_coords.add(tuple(forest_field))
            for f in next_fields:
                adjacent_forest_coords[tuple(f)] += 1.0
