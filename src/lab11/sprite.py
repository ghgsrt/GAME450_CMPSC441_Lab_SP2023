import pygame
import math
from typing import Any, List, Tuple
import torch

from diffusers import StableDiffusionPipeline

model_id = "kohbanye/pixel-art-style"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)


# disable the nsfw filter to avoid black boxes when it inevitably misclassifies
def dummy(images, **_kwargs):
    return images, False


pipe.safety_checker = dummy

prompt = "pixelartstyle, rpg, bandit, robber, holding a weapon, angry"


def generate_image():
    pipe(prompt).images[0].save("assets/ai.png")


def load_image(image_path: str) -> pygame.Surface:
    image = pygame.image.load(image_path).convert_alpha()
    return image


class Sprite:
    def __init__(
        self,
        image_path: str,
        starting_position: Tuple[int, int],
        scaled_size: Tuple[int, int] = (50, 50),
    ) -> None:
        self.sprite_pos: List[float] = list(map(float, starting_position))
        if image_path == "assets/ai.png":
            generate_image()
        self.sprite_image: pygame.Surface = load_image(image_path)
        self.sprite_image = pygame.transform.scale(self.sprite_image, scaled_size)

    def set_location(self, location: Tuple[int, int]) -> None:
        self.sprite_pos = list(map(float, location))

    def move_sprite(self, end_pos: Tuple[int, int], speed: float) -> bool:
        travelling = True
        distance = math.sqrt(
            (end_pos[0] - self.sprite_pos[0]) ** 2
            + (end_pos[1] - self.sprite_pos[1]) ** 2
        )
        direction = (
            (end_pos[0] - self.sprite_pos[0]) / distance,
            (end_pos[1] - self.sprite_pos[1]) / distance,
        )
        self.sprite_pos[0] = self.sprite_pos[0] + direction[0] * speed
        self.sprite_pos[1] = self.sprite_pos[1] + direction[1] * speed
        if (
            end_pos[0] - 5 <= self.sprite_pos[0] <= end_pos[0] + 5
            and end_pos[1] - 5 <= self.sprite_pos[1] <= end_pos[1] + 5
        ):
            travelling = False
            self.sprite_pos = list(map(int, end_pos))
        return travelling

    def draw_sprite(self, screen: Any) -> None:
        screen.blit(self.sprite_image, self.sprite_pos)
        # text_surface = my_font.render(str(self.sprite_pos), True, (0, 0, 150))
        # screen.blit(text_surface, self.sprite_pos)


# import pygame
# import math


# def load_image(image_path):
#     image = pygame.image.load(image_path).convert_alpha()
#     return image


# class Sprite:
#     def __init__(self, image_path, starting_position, scaled_size=(50, 50)) -> None:
#         self.sprite_pos = list(map(float, starting_position))
#         self.sprite_image = load_image(image_path)
#         self.sprite_image = pygame.transform.scale(self.sprite_image, scaled_size)

#     def set_location(self, location):
#         self.sprite_pos = list(map(float, location))

#     def move_sprite(self, end_pos, speed):
#         travelling = True
#         distance = math.sqrt(
#             (end_pos[0] - self.sprite_pos[0]) ** 2
#             + (end_pos[1] - self.sprite_pos[1]) ** 2
#         )
#         direction = (
#             (end_pos[0] - self.sprite_pos[0]) / distance,
#             (end_pos[1] - self.sprite_pos[1]) / distance,
#         )
#         self.sprite_pos[0] = self.sprite_pos[0] + direction[0] * speed
#         self.sprite_pos[1] = self.sprite_pos[1] + direction[1] * speed
#         if (
#             end_pos[0] - 5 <= self.sprite_pos[0] <= end_pos[0] + 5
#             and end_pos[1] - 5 <= self.sprite_pos[1] <= end_pos[1] + 5
#         ):
#             travelling = False
#             self.sprite_pos = list(map(int, end_pos))
#         return travelling

#     def draw_sprite(self, screen):
#         screen.blit(self.sprite_image, self.sprite_pos)
#         # text_surface = my_font.render(str(self.sprite_pos), True, (0, 0, 150))
#         # screen.blit(text_surface, self.sprite_pos)
