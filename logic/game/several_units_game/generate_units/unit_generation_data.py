from dataclasses import dataclass
from logic.game.share.unit_type import UnitType


@dataclass
class UnitGenerationData:
    units_number: int
    unit_type_probs: dict[UnitType, float]=None
    is_fixed_unit_number: bool=False

    def __post_init__(self):
        if self.unit_type_probs is None:
            return

        if len(self.unit_type_probs) != len(UnitType):
            raise ValueError("unit_type_percentages must have an entry for each UnitType")
        sum_percentages = sum(self.unit_type_probs.values())
        if abs(sum_percentages - 1.0) > 1e-6:
            raise ValueError("Sum of unit_type_percentages values must be 1.0")
