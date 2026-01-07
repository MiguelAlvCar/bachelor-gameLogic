import numpy as np

from logic.map.terrain_type import TerrainType
from logic.map.map import Map
from logic.map.coordinates.evenr_to_axial import evenr_to_axial


def generate_cities(map: Map, city_percentage: float):
    weights = np.ones((map.height, map.even_width))

    city_coords = set()

    _add_city(city_coords, weights, map)

    while len(city_coords) < (map.even_width * map.height * city_percentage):
        _add_city(city_coords, weights, map)
        _add_city(city_coords, weights, map)

    map.number_cities = len(city_coords)


def _add_city(city_coords, weights, map: Map):
    probs = weights / weights.sum()
    flat_probs = probs.ravel()
    flat_index = np.random.choice(flat_probs.size, p=flat_probs)
    city = np.unravel_index(flat_index, probs.shape)
    city = evenr_to_axial(np.array([city], dtype=np.int16), map.height)[0]

    if map.terrain_types[city[0], city[1]] == TerrainType.HILL.value:
        map.terrain_types[city[0], city[1]] = TerrainType.HILL_CITY.value
        city_coords.add(tuple(city))
    elif map.terrain_types[city[0], city[1]] == TerrainType.PLAIN.value:
        map.terrain_types[city[0], city[1]] = TerrainType.CITY.value
        city_coords.add(tuple(city))
    else:
        _add_city(city_coords, weights, map)

