from numba import njit


@njit(cache=True)
def valid_coord(coord, mask):
    return coord[0] >= 0 and coord[1] >= 0 and coord[1] < mask.shape[1] and coord[0] < mask.shape[0] and \
           mask[coord[0], coord[1]]
