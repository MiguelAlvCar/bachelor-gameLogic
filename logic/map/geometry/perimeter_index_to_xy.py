def perimeter_index_to_xy(idx, width, height):
    top_len = width
    right_len = height - 1
    bottom_len = width - 1
    left_len = height - 2
    perim = top_len + right_len + bottom_len + left_len

    idx %= perim  # safety

    # Top edge
    if idx < top_len:
        return 0, idx

    idx -= top_len

    # Right edge
    if idx < right_len:
        return idx + 1, width - 1

    idx -= right_len

    # Bottom edge
    if idx < bottom_len:
        return height - 1, (width - 2) - idx

    idx -= bottom_len

    # Left edge
    return (height - 1) - (idx + 1), 0
