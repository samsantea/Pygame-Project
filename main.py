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

        self.planter = False

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

class Bomb(pygame.sprite.Sprite):
    """Bomb

    Attributes:
    image: visual representation
    rect: mathematical representation
    planting_time: how much time is left from beginning to plant until the bomb is set
    plant_speed
    """
    def __init__(self, coords: tuple) -> None:
        """
        Arguments:
            coords: tuple of (x,y) to represent location
        """

        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        self.planting_time = 15.0
        self.plant_speed = 0.0

    def update(self):
        self.planting_time += self.plant_speed

    def plant(self):
        self.plant_speed = -0.1

    def stop_plant(self):
        self.plant_speed = 0.0

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
    time_start_plant = 0.0
    respawn_location = (40, 40)
    round = 1
    allow_defuse = False
    player_one_click = False # Prevents player one from holding down more than one key
    player_two_click = False # Prevents player one from holding down more than one key
    player_one_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_4]
    player_two_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP4]

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

    player_one = Player(respawn_location, RED)
    player_one.planter = True
    player_two = Player((948, 690), BLUE)
    all_sprites.add(player_one)
    all_sprites.add(player_two)
    player_sprites.add(player_one)
    player_sprites.add(player_two)
    time_hit = 0.0

    bomb = Bomb((0, 0))
    all_sprites.add(bomb)

    new_bomb_coords = (-1, -1)
    time_ticking = 0
    time_defuse = 0

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Keys to move player one

            # TODO: optimize code with for loop (if possible)
            if event.type == pygame.KEYDOWN:
                if event.key in player_one_keys and player_one_click == False:
                    player.stop()
                    player_one_click = True
                    if event.key == pygame.K_a:
                        player_one.go_left()
                    elif event.key == pygame.K_d:
                        player_one.go_right()
                    elif event.key == pygame.K_w:
                        player_one.go_up()
                    elif event.key == pygame.K_s:
                        player_one.go_down()
                    elif event.key == pygame.K_4:
                        if player_one.planter == True:
                            bomb.plant()
                            print("planting")
                        elif allow_defuse == True:
                            time_defuse = time.time()

            # Keys to move player two
                elif event.key in player_two_keys and player_two_click == False:
                    player.stop()
                    player_one_click = True
                    if event.key == pygame.K_LEFT:
                        player_two.go_left()
                    elif event.key == pygame.K_RIGHT:
                        player_two.go_right()
                    elif event.key == pygame.K_UP:
                        player_two.go_up()
                    elif event.key == pygame.K_DOWN:
                        player_two.go_down()
                    elif event.key == pygame.K_KP4:
                        if player_two.planter == True:
                            bomb.plant()
                            print("planting")
                        elif allow_defuse == True:
                            time_defuse = time.time()
                            print("defusing")


            elif event.type == pygame.KEYUP:
                if event.key in player_one_keys:
                    player_one_click = False
                    if player_one.x_vel != 0 or player_one.y_vel != 0:
                        player_one.stop()

                    if event.key == pygame.K_4:
                        bomb.stop_plant()
                        time_defuse = 0
                        print("stopped")

                elif event.key in player_two_keys:
                    player_two_click = False
                    if player_two.x_vel != 0 or player_two.y_vel != 0:
                        player_two.stop()

                    if event.key == pygame.K_KP4:
                        bomb.stop_plant()
                        time_defuse = 0
                        print("stopped")

        # ----------- CHANGE ENVIRONMENT

        all_sprites.update()

        # bomb.rect.center = player_one.rect.center

        # See if we hit anything
        for player in player_sprites:
            opponent_hit_list = pygame.sprite.spritecollide(player, player_sprites, False)
            for opponent in opponent_hit_list:
                if opponent != player:
                    if (time.time() - time_hit) >= 5.0:
                        time_hit = time.time()
                        opponent.lives -= 1
                        opponent.rect.toplefts = respawn_location
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

            if player.planter == True and bomb.planting_time > 0:
                bomb.rect.center = player.rect.center

            elif -0.1 <= bomb.planting_time <= 0.0:
                print("planted")
                time_ticking = time.time()
                if new_bomb_coords == (-1, -1):
                    new_bomb_coords = player.rect.center
                    bomb.rect.center = new_bomb_coords

            elif player.planter == False and bomb.planting_time < 1:
                if pygame.sprite.collide_rect(player, bomb):
                    allow_defuse = True
            if time_defuse > 0:
                if time.time() - time_defuse > 10:
                    done = True # TODO: add an endgame message instead of closing game

            if player.lives <= 0:
                done = True # TODO: add an endgame message instead of closing game

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
