# I have pylint uninstalled entirely yet it's still linting, smh VSCode
# pylint: disable-all

"""
Lab 7: Realistic Cities

In this lab you will try to generate realistic cities using a genetic algorithm.
Your cities should not be under water, and should have a realistic distribution across the landscape.
Your cities may also not be on top of mountains or on top of each other.
Create the fitness function for your genetic algorithm, so that it fulfills these criterion
and then use it to generate a population of cities.

Please comment your code in the fitness function to explain how are you making sure each criterion is
fulfilled. Clearly explain in comments which line of code and variables are used to fulfill each criterion.
"""
import matplotlib.pyplot as plt
import pygad
import numpy as np
import heapq
from collections import defaultdict, deque

import sys
from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / ".." / "..").resolve().absolute()))

from src.lab5.landscape import elevation_to_rgba, get_elevation


def game_fitness(cities, idx, elevation, size):
    """
    Create your fitness function here to fulfill the following criteria:
    1. The cities should not be under water
    2. The cities should have a realistic distribution across the landscape
    3. The cities may also not be on top of mountains or on top of each other
    """
    fitness = 300.0001  # Do not return a fitness of 0, it will mess up the algorithm.

    border_threshold = 20
    border_penalty = 120
    distance_threshold = 80
    distance_penalty = 40
    underwater_threshold = 0.35
    underwater_penalty = 70
    mountain_threshold = 0.6
    mountain_penalty = 70

    city_coordinates = [(city // size[1], city % size[1]) for city in cities]
    penalties = [
        underwater_penalty
        if elevation[x, y] < underwater_threshold
        else mountain_penalty
        if elevation[x, y] > mountain_threshold
        else border_penalty
        if any(d <= border_threshold for d in [x, y, size[0] - x, size[1] - y])
        else distance_penalty
        * sum(
            np.sqrt((x - x2) ** 2 + (y - y2) ** 2) < distance_threshold
            for x2, y2 in city_coordinates
            if (x, y) != (x2, y2)
        )
        for x, y in city_coordinates
    ]
    fitness -= sum(penalties)

    return fitness


def setup_GA(fitness_fn, n_cities, size):
    """
    It sets up the genetic algorithm with the given fitness function,
    number of cities, and size of the map

    :param fitness_fn: The fitness function to be used
    :param n_cities: The number of cities in the problem
    :param size: The size of the grid
    :return: The fitness function and the GA instance.
    """
    num_generations = 100
    num_parents_mating = 10

    solutions_per_population = 300
    num_genes = n_cities

    init_range_low = 0
    init_range_high = size[0] * size[1]

    parent_selection_type = "sss"
    keep_parents = 10

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        fitness_func=fitness_fn,
        sol_per_pop=solutions_per_population,
        num_genes=num_genes,
        gene_type=int,
        init_range_low=init_range_low,
        init_range_high=init_range_high,
        parent_selection_type=parent_selection_type,
        keep_parents=keep_parents,
        crossover_type=crossover_type,
        mutation_type=mutation_type,
        mutation_percent_genes=mutation_percent_genes,
    )

    return fitness_fn, ga_instance


def solution_to_cities(solution, size):
    """
    It takes a GA solution and size of the map, and returns the city coordinates
    in the solution.

    :param solution: a solution to GA
    :param size: the size of the grid/map
    :return: The cities are being returned as a list of lists.
    """
    cities = np.array(
        list(map(lambda x: [int(x / size[0]), int(x % size[1])], solution))
    )
    return cities


def show_cities(cities, landscape_pic, cmap="gist_earth"):
    """
    It takes a list of cities and a landscape picture, and plots the cities on top of the landscape

    :param cities: a list of (x, y) tuples
    :param landscape_pic: a 2D array of the landscape
    :param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional)
    """
    cities = np.array(cities)
    plt.imshow(landscape_pic, cmap=cmap)
    plt.plot(cities[:, 1], cities[:, 0], "r.")
    plt.show()


def get_fitness(elevation, size):
    return lambda cities, idx: game_fitness(cities, idx, elevation, size)


def get_spread_cities(size, elevation, n_cities: int):
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    fitness_function, ga_instance = setup_GA(
        get_fitness(elevation, size), n_cities, size
    )

    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)

    ga_instance.run()

    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    print(fitness_function(cities, 0))

    return cities_t


def is_valid(x, y, map_size, elevation_map):
    return 0 <= x < map_size[0] and 0 <= y < map_size[1]
    # if 0 <= x < map_size[0] and 0 <= y < map_size[1]:
    # return 0.35 <= elevation_map[x][y] <= 0.95
    # return False


def heuristic(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current):
    path = deque()
    while current in came_from:
        current = came_from[current]
        path.appendleft(current)
    return list(path)[1:-1]


def cost_function(
    elevation, lower_bound, upper_bound, lower_extreme, upper_extreme, base_cost
):
    if lower_bound <= elevation <= upper_bound:
        return base_cost + abs(elevation - lower_bound) + abs(elevation - upper_bound)
    elif (
        lower_extreme <= elevation < lower_bound
        or upper_bound < elevation <= upper_extreme
    ):
        return (
            base_cost
            + (abs(elevation - lower_bound) + abs(elevation - upper_bound)) * 2
        )
    else:
        return (
            base_cost
            + (
                (abs(elevation - lower_extreme) ** 2)
                + (abs(elevation - upper_extreme) ** 2)
            )
            * 1.5
        )


def scaled_cost(cost, distance, grace_distance):
    scaling_factor = max(0, 1 - distance / grace_distance)
    return cost * (1 - scaling_factor)


def astar(
    start,
    end,
    elevation_map,
    map_size,
    lower_bound,
    upper_bound,
    lower_extreme,
    upper_extreme,
    base_cost,
    grace_distance,
):
    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: heuristic(*start, *end)}
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = reconstruct_path(came_from, current)
            return path, g_score[end]

        neighbors = [
            (current[0] + dx, current[1] + dy)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ]
        valid_neighbors = [
            neighbor
            for neighbor in neighbors
            if is_valid(*neighbor, map_size, elevation_map)
        ]

        for neighbor in valid_neighbors:
            elevation = elevation_map[neighbor[0]][neighbor[1]]
            cost = cost_function(
                elevation,
                lower_bound,
                upper_bound,
                lower_extreme,
                upper_extreme,
                base_cost,
            )
            distance_to_start = heuristic(*neighbor, *start)
            distance_to_end = heuristic(*neighbor, *end)
            grace_distance_factor = min(distance_to_start, distance_to_end)
            scaled_cost_value = scaled_cost(cost, grace_distance_factor, grace_distance)

            tentative_g_score = g_score[current] + scaled_cost_value

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(*neighbor, *end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, None, None


class CrazyDict(defaultdict):
    def __setitem__(self, key, value) -> None:
        return super().__setitem__(tuple(sorted(key)), value)

    def __getitem__(self, key):
        return super().__getitem__(tuple(sorted(key)))


def get_paths(routes, elevation, size, max_distance=100):
    paths = CrazyDict(tuple)

    shortest_paths_dict = CrazyDict(lambda: (None, float("inf"), float("inf")))

    for start, end in routes:
        start = tuple(start)
        end = tuple(end)

        path, cost = astar(
            start,
            end,
            elevation,
            size,
            lower_bound=0.42,
            upper_bound=0.5,
            lower_extreme=0.37,
            upper_extreme=0.65,
            base_cost=1,
            grace_distance=10,
        )

        if path is None:
            continue

        distance = len(path)

        if distance <= max_distance:
            paths[(start, end)] = (path, cost)
        elif distance < shortest_paths_dict[(start, end)][2]:
            shortest_paths_dict[(start, end)] = (path, cost, distance)

    for route, (shortest_path, cost, _distance) in shortest_paths_dict.items():
        if len(paths[route]) == 0 and shortest_path is not None:
            paths[route] = (shortest_path, cost)

    for i, (key, (path, cost)) in enumerate(paths.items()):
        print(f"{i}:  {cost}")

    return paths


if __name__ == "__main__":
    print("Initial Population")

    size = 100, 100
    n_cities = 10
    elevation = get_elevation(size)
    """ initialize elevation here from your previous code"""
    # normalize landscape
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    # setup fitness function and GA

    fitness_function, ga_instance = setup_GA(
        get_fitness(elevation, size), n_cities, size
    )

    # Show one of the initial solutions.
    cities = ga_instance.initial_population[0]
    cities = solution_to_cities(cities, size)
    show_cities(cities, landscape_pic)

    # Run the GA to optimize the parameters of the function.
    ga_instance.run()
    ga_instance.plot_fitness()
    print("Final Population")

    # Show the best solution after the GA finishes running.
    cities = ga_instance.best_solution()[0]
    cities_t = solution_to_cities(cities, size)
    plt.imshow(landscape_pic, cmap="gist_earth")
    plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    plt.show()
    print(fitness_function(cities, 0))
