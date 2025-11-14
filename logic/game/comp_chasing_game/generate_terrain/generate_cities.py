import numpy as np

from logic.map.field_type import FieldType
from logic.map.map import Map

def generate_cities(map: Map, city_percentage: float):
    weights = np.ones((map.height, map.width))

    city_coords = set()

    while len(city_coords) < (map.width * map.height * city_percentage):
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        city = np.unravel_index(flat_index, probs.shape)
        if map.field_types[city[0], city[1]] == FieldType.HILL.value:
            map.field_types[city[0], city[1]] = FieldType.HILL_CITY.value
        elif map.field_types[city[0], city[1]] == FieldType.PLAIN.value:
            map.field_types[city[0], city[1]] = FieldType.CITY.value
        else:
            continue

        city_coords.add(tuple(city))
