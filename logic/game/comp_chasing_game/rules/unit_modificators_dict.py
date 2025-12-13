import numpy as np

from logic.game.comp_chasing_game.rules.unit_modificators import UnitModificators
from logic.game.share.unit_type import UnitType
from logic.map.terrain_type import TerrainType


unit_modificator_dict: dict[UnitType, UnitModificators] = {}

unit_modificator_dict[UnitType.INFANTRY] = UnitModificators(
    movement=1,
    strengh=0.08,
    organisation_vulnerability=2.,
    defend_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 1.5,
        TerrainType.HILL_CITY.value: 1.9,
        TerrainType.HILL.value: 1.35,
        TerrainType.FOREST_HILL.value: 1.6,
        TerrainType.FOREST.value: 1.3
    },
    attack_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 1.,
        TerrainType.HILL_CITY.value: 1.,
        TerrainType.HILL.value: 1.,
        TerrainType.FOREST_HILL.value: 1.,
        TerrainType.FOREST.value: 1.
    },
    movement_bonus_terrain = {
        TerrainType.PLAIN.value: 0,
        TerrainType.CITY.value: 0,
        TerrainType.HILL_CITY.value: 0,
        TerrainType.HILL.value: 0,
        TerrainType.FOREST_HILL.value: 0,
        TerrainType.FOREST.value: 0
    },
    attack_unit = {
        UnitType.INFANTRY.value: 1.,
        UnitType.ANTITANK.value: 1.,
        UnitType.TANK.value: 0.7,
    })

unit_modificator_dict[UnitType.ANTITANK] = UnitModificators(
    movement=2,
    strengh=0.10,
    organisation_vulnerability=2.,
    defend_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 1.3,
        TerrainType.HILL_CITY.value: 1.6,
        TerrainType.HILL.value: 1.35,
        TerrainType.FOREST_HILL.value: 1.4,
        TerrainType.FOREST.value: 1.2
    },
    attack_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 0.9,
        TerrainType.HILL_CITY.value: 0.9,
        TerrainType.HILL.value: 1.,
        TerrainType.FOREST_HILL.value: 0.9,
        TerrainType.FOREST.value: 0.9,
    },
    movement_bonus_terrain = {
        TerrainType.PLAIN.value: 0,
        TerrainType.CITY.value: 0,
        TerrainType.HILL_CITY.value: 0,
        TerrainType.HILL.value: 0,
        TerrainType.FOREST_HILL.value: 0,
        TerrainType.FOREST.value: 0
    },
    attack_unit = {
        UnitType.INFANTRY.value: 0.6,
        UnitType.ANTITANK.value: 0.6,
        UnitType.TANK.value: 2.0,
    })

unit_modificator_dict[UnitType.TANK] = UnitModificators(
    movement=3,
    strengh=0.15,
    organisation_vulnerability=3.5,
    defend_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 0.9,
        TerrainType.HILL_CITY.value: 1.1,
        TerrainType.HILL.value: 1.35,
        TerrainType.FOREST_HILL.value: 1.1,
        TerrainType.FOREST.value: 0.7
    },
    attack_terrain = {
        TerrainType.PLAIN.value: 1.,
        TerrainType.CITY.value: 0.8,
        TerrainType.HILL_CITY.value: 0.8,
        TerrainType.HILL.value: 1.,
        TerrainType.FOREST_HILL.value: 0.8,
        TerrainType.FOREST.value: 0.8
    },
    movement_bonus_terrain = {
        TerrainType.PLAIN.value: 0,
        TerrainType.CITY.value: 0,
        TerrainType.HILL_CITY.value: 1,
        TerrainType.HILL.value: 1,
        TerrainType.FOREST_HILL.value: 0,
        TerrainType.FOREST.value: -1
    },
    attack_unit = {
        UnitType.INFANTRY.value: 1.,
        UnitType.ANTITANK.value: 1.,
        UnitType.TANK.value: 1.,
    })


movements = np.array([unit_modificator_dict[key].movement for key in sorted(unit_modificator_dict)])
movement_bonus_terrain_dicts = [unit_modificator_dict[key].movement_bonus_terrain for key in sorted(unit_modificator_dict)]
movement_bonus_terrain_dicts = [[movement_bonus_terrain[terrain] for terrain in sorted(movement_bonus_terrain)] for movement_bonus_terrain in movement_bonus_terrain_dicts]
movement_bonus_terrain_dicts = np.array(movement_bonus_terrain_dicts)

