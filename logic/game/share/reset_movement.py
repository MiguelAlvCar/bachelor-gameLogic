import numpy as np
import numpy.typing as npt

from logic.game.comp_chasing_game.rules.unit_modificators_dict import movements, movement_bonus_terrain_dicts


def reset_movement(unit_movement: npt.NDArray[np.int8],
                   unit_types: npt.NDArray[np.int8],
                   unit_positions: npt.NDArray[np.int16],
                   terrain_types: npt.NDArray[np.int16]):

    unit_terrain = terrain_types[unit_positions[:,0], unit_positions[:,1]]

    all_movement = movements[unit_types]
    all_movement_bonus = movement_bonus_terrain_dicts[unit_types, unit_terrain]

    unit_movement[:] = all_movement + all_movement_bonus

