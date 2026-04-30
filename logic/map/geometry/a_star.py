from queue import PriorityQueue
from typing import Callable
import numpy as np
import numpy.typing as npt


def a_star(movement_costs: npt.NDArray[np.float32],
           origin: tuple[int, int],
           target: tuple[int, int],
           heuristic: Callable[[tuple[int, int], tuple[int, int]], float],
           get_neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]]):

    start_tuple = tuple(origin)
    frontier = PriorityQueue()
    frontier.put((0, start_tuple))

    came_from = {}
    cost_so_far = {}

    came_from[start_tuple] = None
    cost_so_far[start_tuple] = 0

    while not frontier.empty():
        _, current = frontier.get()

        if np.array_equal(current, target):
            break

        for next_node in get_neighbors(np.array(current)):
            new_cost = cost_so_far[tuple(current)] + movement_costs[next_node[0], next_node[1]]

            next_node_tuple = tuple(next_node)
            if next_node_tuple not in cost_so_far or new_cost < cost_so_far[next_node_tuple]:
                cost_so_far[next_node_tuple] = new_cost
                priority = new_cost + heuristic(target, next_node)
                frontier.put((priority, next_node_tuple))
                came_from[next_node_tuple] = current

    return came_from, cost_so_far
