# Paclorant
# Author: Samantha
# 2022 Version

import time
import random
import pygame
from pygame import mixer

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOUR = (100, 100, 255)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "Paclorant"


class Player(pygame.sprite.Sprite):
    """Describes a block object
    A subclass of pygame.sprite.Sprite

    Attributes:
        image: visual representation of the player's block
        rect: numerical representation of the player's block
        lives: describe how many lives player one has
        x_vel: x velocity
        y_vel: y velocity
    """

    def __init__(self, coords: tuple, color) -> None:
        """
        Arguments:
            coords: tuple of (x,y) to represent initial location
            color: color of the player
        """

        # Call the superclass constructor
        super().__init__()

        # Create the image of the block
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)

        # Based on the image, create a Rect for the block
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = coords

        # Initial lives
        self.lives = 3

        # Velocity
        self.x_vel = 3
        self.y_vel = 3

    # Movement controlled by the player

    def move(self):


# class Wall(pygame.sprite.Sprite):
#     """Wall
#
#     Attributes:
#         image: visual representation
#         rect: mathematical representation
#     """
#
#     def __init__(self, width: int, height: int, coords: tuple) -> None:
#         """
#         Arguments:
#             width: width of the wall
#             height: height of the wall
#             coords: tuple of (x,y) to represent location
#         """
#
#         # Call the superclass constructor
#         super().__init__()
#
#         self.image = pygame.Surface((width, height))
#         self.image.fill(RED)  # TODO: choose a colour you like
#
#         # Based on the image, create a Rect for the block
#         self.rect = self.image.get_rect()
#
#         # Set the top left of the wall to be at coords
#         self.rect.topleft = coords


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()
    player_one_wins = 0
    player_two_wins = 0
    time_start = time.time()
    time_introduction = 7
    time_invincible = 3

    # Create a group of sprites to hold Sprites
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    player_one = Player((0, 0), RED)
    all_sprites.add(player_one)

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----------- CHANGE ENVIRONMENT

        # ----------- DRAW THE ENVIRONMENT
        screen.fill(BGCOLOUR)  # fill with bgcolor

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()
