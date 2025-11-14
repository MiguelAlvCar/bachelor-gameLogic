from logic.game.comp_chasing_game.generate_terrain.generate_forests import generate_forests
from logic.game.comp_chasing_game.generate_terrain.generate_hills import generate_hills
from logic.game.comp_chasing_game.generate_terrain.generate_cities import generate_cities
from logic.map.map import Map

def generate_terrain(map: Map, hills_percentage: float, forest_percentage: float, city_percentage: float):
    generate_hills(map, hills_percentage)
    generate_forests(map, forest_percentage)
    generate_cities(map, city_percentage)
