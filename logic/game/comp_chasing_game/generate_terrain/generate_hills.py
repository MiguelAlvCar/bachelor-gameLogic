import random
import numpy as np

from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.terrain_type import TerrainType
from logic.map.geometry.find_valid_circumference import find_valid_circumference
from logic.map.geometry.find_hex_line import find_hex_line
from logic.map.map import Map
from logic.map.coordinates.get_playable_fields import get_playable_fields
from logic.map.coordinates.valid_coords import valid_coords

def generate_hills(map: Map, hills_percentage: float):
    max_hill_length = 7
    paddedHeight = map.height + 2 * max_hill_length

    weights = np.ones((map.height, map.even_width))

    hill_coordinates = set()

    paddedWidth = map.even_width + 2 * max_hill_length
    paddedHeight = map.height + 2 * max_hill_length

    playable_fields = get_playable_fields(paddedWidth, paddedHeight)

    while len(hill_coordinates) < (map.even_width * map.height * hills_percentage):
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        line_begin = np.unravel_index(flat_index, probs.shape)
        line_begin = np.array([line_begin[0] + max_hill_length, line_begin[1] + max_hill_length])
        hill_line_length = random.randint(1, max_hill_length)

        circumference_fields = find_valid_circumference(line_begin, playable_fields, radius=hill_line_length)
        line_end = circumference_fields[np.random.choice(len(circumference_fields))]

        line_begin = evenr_to_axial(line_begin.reshape(1, 2), paddedHeight)[0]
        line_end = evenr_to_axial(line_end.reshape(1, 2), paddedHeight)[0]
        line = find_hex_line(line_begin, line_end)
        line = np.array(line)
        line = line - max_hill_length
        line = line[valid_coords(line, map.playable_fields)]
        map.terrain_types[line[:, 0], line[:, 1]] = TerrainType.HILL.value

        for c in line:
            hill_coordinates.add(tuple(c))




