import random
import numpy as np

from logic.map.coordinates.axial_to_evenr import axial_to_evenr
from logic.map.coordinates.evenr_to_axial import evenr_to_axial
from logic.map.field_type import FieldType
from logic.map.geometry.find_circumference import find_circumference
from logic.map.geometry.find_hex_line import find_hex_line
from logic.map.map import Map

def generate_hills(map: Map, hills_percentage: float):
    max_hill_length = 7

    weights = np.ones((map.height, map.width))

    hill_coordinates = set()

    while len(hill_coordinates) < (map.width * map.height * hills_percentage):
        probs = weights / weights.sum()
        flat_probs = probs.ravel()
        flat_index = np.random.choice(flat_probs.size, p=flat_probs)
        line_begin = np.unravel_index(flat_index, probs.shape)
        line_begin = np.array([line_begin[0] + max_hill_length - 1, line_begin[1] + max_hill_length - 1])
        hill_line_length = random.randint(1, max_hill_length)

        circumference_fields = find_circumference(line_begin,
                                                  map.width + 2 * (max_hill_length - 1), map.height + 2 * (max_hill_length - 1),
                                                  radius=hill_line_length)
        line_end = circumference_fields[np.random.choice(len(circumference_fields))]

        axial_origin = evenr_to_axial(line_begin)
        axial_end = evenr_to_axial(line_end)
        line = find_hex_line(axial_origin, axial_end)
        line = np.array([axial_to_evenr(coord) for coord in line])
        line = line - (max_hill_length - 1)
        line = line[(line[:, 0] >= 0) & (line[:, 1] >= 0) & (line[:, 0] < map.height) & (line[:, 1] < map.width)]
        map.field_types[line[:, 0], line[:, 1]] = FieldType.HILL.value

        for c in line:
            hill_coordinates.add(tuple(c))




