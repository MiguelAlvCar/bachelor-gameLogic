import numpy as np
import numpy.typing as npt

class Map:
    def __init__(self, width: int, height: int):
        # First bool value: PLAIN
        self.field_types: npt.NDArray[np.bool_] = np.ones((height, width, 1), dtype=np.bool_)
