'''
Lab 5: PCG and Project Lab

This a combined procedural content generation and project lab. 
You will be creating the static components of the game that will be used in the project.
Use the landscape.py file to generate a landscape for the game using perlin noise.
Use the lab 2 cities_n_routes.py file to generate cities and routes for the game.
Draw the landscape, cities and routes on the screen using pygame.draw functions.
Look for triple quotes for instructions on what to do where.
The intention of this lab is to get you familiar with the pygame.draw functions, 
use perlin noise to generate a landscape and more importantly,
build a mindset of writing modular code.
This is the first time you will be creating code that you may use later in the project.
So, please try to write good modular code that you can reuse later.
You can always write non-modular code for the first time and then refactor it later.
'''

import sys
import pygame
import random
import itertools as it
import numpy as np
from landscape import get_landscape

from pathlib import Path
sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab3.travel_cost import route_to_coordinates

# TODO: Demo blittable surface helper function

''' Create helper functions here '''

def draw_nodes(locs, node_dims, color):
    for loc in locs:
        pygame.draw.rect(screen, color, [*loc, node_dims, node_dims ])

def get_full_route(route_coordinate):
    def sign(num):
        return 1 if num > 0 else -1 if num < 0 else 0

    start_cell, end_cell = route_coordinate
    dist_x, dist_y = (end_cell[0] - start_cell[0], end_cell[1] - start_cell[1])
    sign_x, sign_y = (sign(dist_x), sign(dist_y))
    num_moves_x, num_moves_y = (abs(dist_x), abs(dist_y))

    it_num_moves = it.zip_longest(
        range(num_moves_x),
        range(num_moves_y),
        fillvalue=min(num_moves_x, num_moves_y)
    )

    return [
        (
            (start_cell[0] + (sign_x * i)),
            (start_cell[1] + (sign_y * j))
        )
        for i, j in it_num_moves
    ]

if __name__ == "__main__":
    pygame.init()
    size = width, height = 640, 480
    black = 1, 1, 1

    screen = pygame.display.set_mode(size)
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])

    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta',
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    city_locations = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(city_names)

    ''' Setup cities and routes in here'''

    # city_locations_dict = {name: location for name, location in zip(city_names, city_locations)}
    random.shuffle(routes)
    routes = routes[:10]

    route_coordinates = route_to_coordinates(city_locations, city_names, routes)
    route_paths = [get_full_route(coord) for coord in route_coordinates]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill('black')
        screen.blit(pygame_surface, (0, 0))

        ''' draw cities '''
        draw_nodes(city_locations, 15, 'black')

        ''' draw first 10 routes '''
        for path in route_paths:
            draw_nodes(path, 4, '#9C661F')

        pygame.display.update()
        pygame.display.flip()
