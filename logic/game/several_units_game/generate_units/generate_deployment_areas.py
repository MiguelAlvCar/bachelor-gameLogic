import random

from logic.map.map import Map
from logic.map.geometry.perimeter_index_to_xy import perimeter_index_to_xy
from logic.map.geometry.expand_area import expand_area


def generate_deployment_areas(map: Map):
    if map.width * map.height < 200:
        deployment_area_size = 20
    else:
        deployment_area_size = map.width * map.height // 10

    perimeter_length = 2 * map.width + 2 * map.height - 4
    blue_area_start_index = random.choices(range(perimeter_length))[0]
    blue_area_start = perimeter_index_to_xy(blue_area_start_index, map.width, map.height)

    red_area_start = perimeter_index_to_xy((blue_area_start_index + perimeter_length // 2) % perimeter_length, map.width, map.height)

    rate = 4

    blue_area = expand_area(deployment_area_size, blue_area_start, map.width, map.height, rate)
    red_area = expand_area(deployment_area_size, red_area_start, map.width, map.height, rate)

    return blue_area, red_area
