'''
Lab 2: Cities and Routes

In the final project, you will need a bunch of cities spread across a map. Here you
will generate a bunch of cities and all possible routes between them.
'''
import random
from itertools import combinations

def city_choices(size, k):
    return zip(
        random.choices(range(size[0]), k=k),
        random.choices(range(size[1]), k=k)
    )

def get_randomly_spread_cities(size, n_cities):
    """
    > This function takes in the size of the map and the number of cities to be generated
    and returns a list of cities with their x and y coordinates. The cities are randomly spread
    across the map.

    :param size: the size of the map as a tuple of 2 integers
    :param n_cities: The number of cities to generate
    :return: A list of cities with random x and y coordinates.
    """

    city_locs = set(city_choices(size, n_cities))
    n_city_locs = len(city_locs)
    while n_city_locs < n_cities:
        city_locs.update(city_choices(size, n_cities - n_city_locs))
        n_city_locs = len(city_locs)

    return list(city_locs)

def get_routes(city_names):
    """
    It takes a list of cities and returns a list of all possible routes between those cities.
    Equivalently, all possible routes is just all the possible pairs of the cities.

    :param cities: a list of city names
    :return: A list of tuples representing all possible links between cities/ pairs of cities,
            each item in the list (a link) represents a route between two cities.
    """

    return list(combinations(city_names, 2))

def main():
    """
    Main entrance to the program.
    """

    city_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    cities = get_randomly_spread_cities((100, 200), len(city_names))
    routes = get_routes(city_names)

    print('Cities:')
    for i, city in enumerate(cities):
        print(f'{city_names[i]}: {city}')

    print('Routes:')
    for i, route in enumerate(routes):
        print(f'{i}: {route[0]} to {route[1]}')

if __name__ == '__main__':
    main()
