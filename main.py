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
        self.image = pygame.Surface((35, 35))
        self.image.fill(color)

        # Based on the image, create a Rect for the block
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = coords

        # Initial lives
        self.lives = 3

        # Velocity
        self.x_vel = 0
        self.y_vel = 0

    def update(self):
        """ Update the player location"""
        # Move along the x axis
        self.rect.x += self.x_vel

        # Move along the y axis
        self.rect.y += self.y_vel

    def go_left(self):
        """ Called when the user holds the key to move left"""
        self.x_vel = -3

    def go_right(self):
        """  Called when the user holds the key to move right"""
        self.x_vel = 3

    def go_up(self):
        """  Called when the user holds the key to move up"""
        self.y_vel = -3

    def go_down(self):
        """  Called when the user holds the key to move down"""
        self.y_vel = 3

    def stop(self):
        """Stop the player"""
        self.x_vel = 0
        self.y_vel = 0

class Wall(pygame.sprite.Sprite):
    """Wall

    Attributes:
        image: visual representation
        rect: mathematical representation
    """

    def __init__(self, width: int, height: int, coords: tuple) -> None:
        """
        Arguments:
            width: width of the wall
            height: height of the wall
            coords: tuple of (x,y) to represent location
        """

        # Call the superclass constructor
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)  # TODO: choose a colour you like

        # Based on the image, create a Rect for the block
        self.rect = self.image.get_rect()

        # Set the top left of the wall to be at coords
        self.rect.topleft = coords

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
    wall_attributes = [
        [40, 354, (0, 0)],
        [40, 354, (0, 414)],
        [40, 354, (984, 0)],
        [40, 354, (984, 414)],
        [1024, 40, (0, 0)],
        [1024, 40, (0, 728)],
        [40, 350, (90, 90)],
        [200, 40, (90, 90)],
        [40, 350, (180, 180)],
        [400, 40, (100, 580)],
        [500, 40, (400, 110)]
    ]

    # Create a group of sprites to hold Sprites
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    for attribute in wall_attributes:
        wall = Wall(*attribute)

        wall_sprites.add(wall)
        all_sprites.add(wall)

    player_one = Player((40, 40), RED)
    player_two = Player((948, 690), BLUE)
    all_sprites.add(player_one)
    all_sprites.add(player_two)
    player_sprites.add(player_one)
    player_sprites.add(player_two)

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Keys to move player one
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_one.go_left()
                if event.key == pygame.K_d:
                    player_one.go_right()
                if event.key == pygame.K_w:
                    player_one.go_up()
                if event.key == pygame.K_s:
                    player_one.go_down()

            # Keys to move player two
                if event.key == pygame.K_LEFT:
                    player_two.go_left()
                elif event.key == pygame.K_RIGHT:
                    player_two.go_right()
                elif event.key == pygame.K_UP:
                    player_two.go_up()
                elif event.key == pygame.K_DOWN:
                    player_two.go_down()

            if event.type == pygame.KEYUP:
                # Stops player one when the user lifts up any keys in [W,A,S,D]
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    if player_one.x_vel != 0:
                        player_one.stop()
                    elif player_one.y_vel != 0:
                        player_one.stop()

                # Stops player two when the user lifts up any arrow keys
                elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    if player_two.x_vel != 0:
                        player_two.stop()
                    elif player_two.y_vel != 0:
                        player_two.stop()

        # ----------- CHANGE ENVIRONMENT

        all_sprites.update()

        # See if we hit anything
        for player in player_sprites:
            opponent_hit_list = pygame.sprite.spritecollide(player, player_sprites, False)
            for opponent in opponent_hit_list:
                if opponent != player:
                    time_hit = time.time()
                    opponent.lives -= 1
                    print(opponent)
            block_hit_list = pygame.sprite.spritecollide(player, wall_sprites, False) # TODO: fix teleportation bug
            for block in block_hit_list:
                # If the player is moving right,
                # Set their right side to the left side of the block hit
                if player.x_vel > 0 and block.rect.left <= player.rect.right < block.rect.right:
                    player.stop()
                    player.rect.right = block.rect.left
                elif player.x_vel < 0 and block.rect.right >= player.rect.left > block.rect.left:
                    # If the player is moving left, do the opposite
                    player.stop()
                    player.rect.left = block.rect.right

                elif player.y_vel > 0 and block.rect.top <= player.rect.bottom < block.rect.bottom:
                    # If the player is moving down,
                    # Set their bottom side to the top of the block hit
                    player.stop()
                    player.rect.bottom = block.rect.top
                elif player.y_vel < 0 and block.rect.bottom >= player.rect.top > block.rect.top:
                    player.stop()
                    player.rect.top = block.rect.bottom

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
