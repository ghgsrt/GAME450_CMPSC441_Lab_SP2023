import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg, elevation_to_rgba, get_elevation
from pygame_ai_player import PyGameAIPlayer
from dialogue import Dialogue

from pathlib import Path
from typing import List, Tuple

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab7.ga_cities import get_spread_cities, get_paths

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size: Tuple[int, int], landscape) -> pygame.Surface:
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size: Tuple[int, int]) -> pygame.Surface:
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width: int, height: int, caption: str) -> pygame.Surface:
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(
    city_locations: List[Tuple[int, int]], city_names: List[str]
) -> None:
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


def displayJournal():
    text_list = []
    for entry in dialog.journal:
        text_list.append(game_font.render(entry, True, (0, 0, 150)))

    text_bg = pygame.Rect(20, 20, 250, 360)

    text_y = text_bg.bottom - game_font.get_height()
    for text in reversed(text_list):
        if text_y <= text_bg.top:
            text_list.remove(text)
        else:
            screen.blit(text, (text_bg.left + 10, text_y))
        text_y -= game_font.get_height()
        screen.blit(text, (text_bg.left + 10, text_y))

    pygame.draw.rect(screen, (164, 164, 164), text_bg, 5)
    screen.set_clip(None)


class State:
    def __init__(
        self,
        current_city: int,
        destination_city: int,
        travelling: bool,
        encounter_event: bool,
        cities: List[Tuple[int, int]],
        routes: List[Tuple[Tuple[int, int], Tuple[int, int]]],
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    screen = setup_window(width, height, "Game World Gen Practice")

    elevation = get_elevation(size)
    landscape = elevation_to_rgba(elevation)

    landscape_surface = get_landscape_surface(size, landscape)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_spread_cities(size, elevation, len(city_names))
    # cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)
    routes = get_paths(routes, list(elevation), size)

    # random.shuffle(routes)
    # routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""
    # player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    dialog = Dialogue()

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                print(destination)
                print(
                    dialog.prompt(
                        "player", "Briefly ponder how you are about to travel."
                    )
                )
                # print("Cost: ", routes[(start, destination)][1])
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for route in routes:
            for coord in routes[route][0]:
                pygame.draw.line(screen, (100, 100, 0), coord, coord)

            # for i in range(len(path) - 1):
            #     print(path[i], path[i + 1])
            #     pygame.draw.line(screen, (100, 100, 0), path[i], path[i + 1])
            # pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print("Arrived at", state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            dialog.prompt(
                "generic_enemy",
                "You've come across an elf you can rob! Say something intimidating!",
            )
            run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print("You have reached the end of the game!")
            break


# import sys
# import pygame
# import random
# from sprite import Sprite
# from pygame_combat import run_pygame_combat
# from pygame_human_player import PyGameHumanPlayer
# from landscape import get_landscape, get_combat_bg
# from pygame_ai_player import PyGameAIPlayer

# from pathlib import Path

# sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

# from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


# pygame.font.init()
# game_font = pygame.font.SysFont("Comic Sans MS", 15)


# def get_landscape_surface(size):
#     landscape = get_landscape(size)
#     print("Created a landscape of size", landscape.shape)
#     pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
#     return pygame_surface


# def get_combat_surface(size):
#     landscape = get_combat_bg(size)
#     print("Created a landscape of size", landscape.shape)
#     pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
#     return pygame_surface


# def setup_window(width, height, caption):
#     pygame.init()
#     window = pygame.display.set_mode((width, height))
#     pygame.display.set_caption(caption)
#     return window


# def displayCityNames(city_locations, city_names):
#     for i, name in enumerate(city_names):
#         text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
#         screen.blit(text_surface, city_locations[i])


# class State:
#     def __init__(
#         self,
#         current_city,
#         destination_city,
#         travelling,
#         encounter_event,
#         cities,
#         routes,
#     ):
#         self.current_city = current_city
#         self.destination_city = destination_city
#         self.travelling = travelling
#         self.encounter_event = encounter_event
#         self.cities = cities
#         self.routes = routes


# if __name__ == "__main__":
#     size = width, height = 640, 480
#     black = 1, 1, 1
#     start_city = 0
#     end_city = 9
#     sprite_path = "assets/lego.png"
#     sprite_speed = 1

#     screen = setup_window(width, height, "Game World Gen Practice")

#     landscape_surface = get_landscape_surface(size)
#     combat_surface = get_combat_surface(size)
#     city_names = [
#         "Morkomasto",
#         "Morathrad",
#         "Eregailin",
#         "Corathrad",
#         "Eregarta",
#         "Numensari",
#         "Rhunkadi",
#         "Londathrad",
#         "Baernlad",
#         "Forthyr",
#     ]

#     cities = get_randomly_spread_cities(size, len(city_names))
#     routes = get_routes(cities)

#     random.shuffle(routes)
#     routes = routes[:10]

#     player_sprite = Sprite(sprite_path, cities[start_city])

#     player = PyGameHumanPlayer()

#     """ Add a line below that will reset the player variable to
#     a new object of PyGameAIPlayer class."""
#     player = PyGameAIPlayer()

#     state = State(
#         current_city=start_city,
#         destination_city=start_city,
#         travelling=False,
#         encounter_event=False,
#         cities=cities,
#         routes=routes,
#     )

#     while True:
#         action = player.selectAction(state)
#         if 0 <= int(chr(action)) <= 9:
#             if int(chr(action)) != state.current_city and not state.travelling:
#                 start = cities[state.current_city]
#                 state.destination_city = int(chr(action))
#                 destination = cities[state.destination_city]
#                 player_sprite.set_location(cities[state.current_city])
#                 state.travelling = True
#                 print(
#                     "Travelling from", state.current_city, "to", state.destination_city
#                 )

#         screen.fill(black)
#         screen.blit(landscape_surface, (0, 0))

#         for city in cities:
#             pygame.draw.circle(screen, (255, 0, 0), city, 5)

#         for line in routes:
#             pygame.draw.line(screen, (255, 0, 0), *line)

#         displayCityNames(cities, city_names)
#         if state.travelling:
#             state.travelling = player_sprite.move_sprite(destination, sprite_speed)
#             state.encounter_event = random.randint(0, 1000) < 2
#             if not state.travelling:
#                 print('Arrived at', state.destination_city)

#         if not state.travelling:
#             encounter_event = False
#             state.current_city = state.destination_city

#         if state.encounter_event:
#             run_pygame_combat(combat_surface, screen, player_sprite)
#             state.encounter_event = False
#         else:
#             player_sprite.draw_sprite(screen)
#         pygame.display.update()
#         if state.current_city == end_city:
#             print('You have reached the end of the game!')
#             break
