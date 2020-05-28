import math
import queue as Q

from classes.location_grid import LocationGrid


class Node:
    def __init__(self, previous, coordinates: tuple):
        self.previous = previous
        self.coordinates = coordinates
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __lt__(self, other):
        return self.f < other.f


def informed_search(graph: LocationGrid, start_coords: tuple, end_coords: tuple) -> list:
    open_list = Q.PriorityQueue()
    closed_list = []

    start_coords = check_coordinates_validity(start_coords, graph)
    end_coords = check_coordinates_validity(end_coords, graph)

    initial_node = Node(None, start_coords)
    final_node = Node(None, end_coords)
    current_node: Node
    path = []

    while open_list.qsize() > 0:
        current_node = open_list.get_nowait()

        closed_list.append(current_node)

        if current_node == final_node:
            while current_node != initial_node:
                path.append(current_node)

                current_node = current_node.previous

            path.append(initial_node)

            return path[::-1]

        (x_coord, y_coord) = current_node.coordinates

        possible_moves = find_valid_moves(x_coord, y_coord, graph)

        for move in possible_moves:
            next_node = Node(current_node, move)

            move_cost = get_move_cost(current_node.coordinates, next_node.coordinates, graph)

            if next_node not in closed_list:
                next_node.h = math.hypot(next_node.coordinates[0] - final_node.coordinates[0],
                                         next_node.coordinates[1] - final_node.coordinates[1])
                next_node.g = current_node.g + move_cost
                next_node.f = next_node.h + next_node.g

                for node in open_list.queue:
                    if next_node == node and next_node.f < node.f:
                        open_list.put_nowait(next_node)


# noinspection DuplicatedCode
def find_valid_moves(x_coord, y_coord, graph) -> list:
    possible_moves = []

    if x_coord != graph.x_axis_ticks[0] and x_coord != graph.x_axis_ticks[-1] + graph.grid_size \
            and y_coord != graph.y_axis_ticks[0] and y_coord != graph.y_axis_ticks[-1] + graph.grid_size:
        if (x_coord, y_coord + graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord, y_coord + graph.grid_size))

        if (x_coord + graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord + graph.grid_size, y_coord + graph.grid_size))

        if (x_coord + graph.grid_size, y_coord) not in graph.invalid_coordinates:
            possible_moves.append((x_coord + graph.grid_size, y_coord))

        if (x_coord + graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord + graph.grid_size, y_coord - graph.grid_size))

        if (x_coord, y_coord - graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord, y_coord - graph.grid_size))

        if (x_coord - graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord - graph.grid_size, y_coord - graph.grid_size))

        if (x_coord - graph.grid_size, y_coord) not in graph.invalid_coordinates:
            possible_moves.append((x_coord - graph.grid_size, y_coord))

        if (x_coord - graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
            possible_moves.append((x_coord - graph.grid_size, y_coord + graph.grid_size))

    elif (x_coord == graph.x_axis_ticks[0] or x_coord == graph.x_axis_ticks[-1] + graph.grid_size) \
            != (y_coord == graph.y_axis_ticks[0] or y_coord == graph.y_axis_ticks[-1] + graph.grid_size):
        if y_coord == graph.y_axis_ticks[0]:
            if (x_coord - graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord + graph.grid_size))

            if (x_coord, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord, y_coord + graph.grid_size))

            if (x_coord + graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord + graph.grid_size))

        elif y_coord == graph.y_axis_ticks[-1] + graph.grid_size:
            if (x_coord + graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord - graph.grid_size))

            if (x_coord, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord, y_coord - graph.grid_size))

            if (x_coord - graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord - graph.grid_size))

        elif x_coord == graph.x_axis_ticks[0]:
            if (x_coord + graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord + graph.grid_size))

            if (x_coord + graph.grid_size, y_coord) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord))

            if (x_coord + graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord - graph.grid_size))

        else:
            if (x_coord - graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord - graph.grid_size))

            if (x_coord - graph.grid_size, y_coord) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord))

            if (x_coord - graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord + graph.grid_size))

    else:
        if x_coord == graph.x_axis_ticks[0] and y_coord == graph.y_axis_ticks[0]:
            if (x_coord + graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord + graph.grid_size))

        elif x_coord == graph.x_axis_ticks[0] and y_coord == graph.y_axis_ticks[-1] + graph.grid_size:
            if (x_coord + graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord + graph.grid_size, y_coord - graph.grid_size))

        elif x_coord == graph.x_axis_ticks[-1] + graph.grid_size and y_coord == graph.y_axis_ticks[0]:
            if (x_coord - graph.grid_size, y_coord + graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord + graph.grid_size))

        elif x_coord == graph.x_axis_ticks[-1] + graph.grid_size \
                and y_coord == graph.y_axis_ticks[-1] + graph.grid_size:
            if (x_coord - graph.grid_size, y_coord - graph.grid_size) not in graph.invalid_coordinates:
                possible_moves.append((x_coord - graph.grid_size, y_coord - graph.grid_size))

    return possible_moves


def get_move_cost(source, target, graph) -> float:
    if source[0] == target[0] or source[1] == target[1]:
        for block in graph.blocked_blocks:
            if source[0] and source[1] and target[0] and target[1] in block:
                return 1.3
        return 1
    else:
        return 1.5


def check_coordinates_validity(coords: tuple, graph) -> tuple:
    x_coord = coords[0]
    y_coord = coords[1]

    if x_coord not in graph.x_axis_ticks:
        for i, tick in enumerate(graph.x_axis_ticks):
            if x_coord < tick:
                x_coord = graph.x_axis_ticks[i - 1]
                break

    if y_coord not in graph.y_axis_ticks:
        for i, tick in enumerate(graph.y_axis_ticks):
            if y_coord < tick:
                y_coord = graph.y_axis_ticks[i - 1]
                break

    return x_coord, y_coord
