from dataclasses import dataclass
from logic.game.share.unit_type import UnitType


@dataclass
class UnitModificators:
    movement: int
    strengh: float
    organisation_vulnerability: float
    defend_terrain: dict[int, float]
    attack_terrain: dict[int, float]
    movement_bonus_terrain: dict[int, int]
    attack_unit: dict[int, float]
