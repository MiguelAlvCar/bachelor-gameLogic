from logic.map.terrain_type import TerrainType


movement_cost: dict[int, int] = {
        TerrainType.PLAIN.value: 1,
        TerrainType.CITY.value: 1,
        TerrainType.HILL_CITY.value: 2,
        TerrainType.HILL.value: 2,
        TerrainType.FOREST_HILL.value: 3,
        TerrainType.FOREST.value: 3
    }
