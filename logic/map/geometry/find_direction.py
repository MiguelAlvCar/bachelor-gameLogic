from numba import njit


@njit(cache=True)
def find_direction(origin, target):
    delta_x = target[0] - origin[0]
    delta_y = target[1] - origin[1]

    if delta_x == -1 and delta_y == 0:
        return 0
    elif delta_x == 0 and delta_y == -1:
        return 1
    elif delta_x == 1 and delta_y == -1:
        return 2
    elif delta_x == 1 and delta_y == 0:
        return 3
    elif delta_x == 0 and delta_y == 1:
        return 4
    elif delta_x == -1 and delta_y == 1:
        return 5
    else:
        raise ValueError(f"Origin {origin} and target {target} are not neighboring fields")
