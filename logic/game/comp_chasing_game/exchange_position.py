def exchange_positions(unit_index1, unit_index2, unit_positions, map_positions):
    old_position1 = unit_positions[unit_index1].copy()
    old_position2 = unit_positions[unit_index2]
    map_positions[old_position2[0], old_position2[1]] = unit_index1
    map_positions[old_position1[0], old_position1[1]] = unit_index2
    unit_positions[unit_index1] = old_position2
    unit_positions[unit_index2] = old_position1
