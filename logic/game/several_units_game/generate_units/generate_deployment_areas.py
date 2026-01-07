import random
import numpy as np

from logic.map.map import Map
from logic.map.geometry.perimeter_index_to_xy import perimeter_index_to_xy
from logic.map.geometry.expand_area import expand_area
from logic.map.coordinates.evenr_to_axial import evenr_to_axial


def generate_deployment_areas(map: Map):
    if map.even_width * map.height < 200:
        deployment_area_size = 20
    else:
        deployment_area_size = map.even_width * map.height // 10

    perimeter_length = 2 * map.even_width + 2 * map.height - 4
    blue_area_start_index = random.choices(range(perimeter_length))[0]
    blue_area_start = perimeter_index_to_xy(blue_area_start_index, map.even_width, map.height)

    red_area_start = perimeter_index_to_xy((blue_area_start_index + perimeter_length // 2) % perimeter_length, map.even_width, map.height)

    blue_area_start = evenr_to_axial(np.array([blue_area_start], dtype=np.int16), map.height)[0]
    red_area_start = evenr_to_axial(np.array([red_area_start], dtype=np.int16), map.height)[0]

    rate = 4

    blue_area = expand_area(deployment_area_size, blue_area_start, map.playable_fields, rate)
    red_area = expand_area(deployment_area_size, red_area_start, map.playable_fields, rate)

    return blue_area, red_area
