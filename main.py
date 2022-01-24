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
        wins: how many rounds the player has won
        planter: determines whether the player is the bomb planter
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

        self.is_planter = False

        self.wins = 0

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

        self.reset()

    def reset(self):
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
    planter_wins = 0
    defender_wins = 0
    time_start = time.time()
    time_introduction = 7
    time_invincible = 3
    time_start_plant = 0.0
    game_state = "running"
    planter_click = False # Prevents player one from holding down more than one key
    defender_click = False # Prevents player one from holding down more than one key
    planter_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_4]
    defender_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP4]
    planter_spawn = (40, 40)
    defender_spawn = (948, 690)

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
        [500, 40, (400, 110)],
        [40, 300, (650, 200)],
        [250, 40, (650, 500)],
        [40, 160, (860, 380)]
    ]


    # Create a group of sprites to hold Sprites
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    for attribute in wall_attributes:
        wall = Wall(*attribute)

        wall_sprites.add(wall)
        all_sprites.add(wall)

    planter = Player(planter_spawn, RED)
    planter.is_planter = True
    defender = Player(defender_spawn, BLUE)
    all_sprites.add(planter)
    all_sprites.add(defender)
    player_sprites.add(planter)
    player_sprites.add(defender)
    time_hit = 0.0
    time_round_end = 0.0
    time_start = 0

    bomb = Bomb(planter.rect.center)
    all_sprites.add(bomb)

    new_bomb_coords = (-1, -1)
    time_ticking = 0.0
    time_defuse = 0

    font = pygame.font.SysFont("Arial", 25)
    big_font = pygame.font.SysFont("Arial", 40)

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Keys to move player one
            if game_state == "running":
                if event.type == pygame.KEYDOWN:
                    if event.key in planter_keys and planter_click == False:
                        planter.stop()
                        planter_click = True
                        if event.key == pygame.K_a:
                            planter.go_left()
                        elif event.key == pygame.K_d:
                            planter.go_right()
                        elif event.key == pygame.K_w:
                            planter.go_up()
                        elif event.key == pygame.K_s:
                            planter.go_down()
                        elif event.key == pygame.K_4 and planter.is_planter == True:
                            bomb.plant()
                            print("planting")

                # Keys to move player two
                    elif event.key in defender_keys and defender_click == False:
                        defender.stop()
                        defender_click = True
                        if event.key == pygame.K_LEFT:
                            defender.go_left()
                        elif event.key == pygame.K_RIGHT:
                            defender.go_right()
                        elif event.key == pygame.K_UP:
                            defender.go_up()
                        elif event.key == pygame.K_DOWN:
                            defender.go_down()
                        elif event.key == pygame.K_KP4 and allow_defuse == True:
                            time_defuse = time.time()
                            print("defusing")


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_4:
                        bomb.stop_plant()
                        print("stopped plant")

                    if event.key in planter_keys:
                        planter_click = False
                        if planter.x_vel != 0 or planter.y_vel != 0:
                            planter.stop()
                    elif event.key in defender_keys:
                        defender_click = False
                        if defender.x_vel != 0 or defender.y_vel != 0:
                            defender.stop()

                        if event.key == pygame.K_KP4:
                            time_defuse = 0
                            print("stopped")

        # ----------- CHANGE ENVIRONMENT

        all_sprites.update()

        if game_state == "running":
            # See if we hit anything
            for player in player_sprites:
                if 354 < player.rect.y <= player.rect.y <= 414:
                    if player.rect.right <= 0:
                        player.rect.left = SCREEN_WIDTH
                    elif player.rect.left >= SCREEN_WIDTH:
                        player.rect.right = 0

                opponent_hit = pygame.sprite.spritecollide(player, player_sprites, False)
                for opponent in opponent_hit:
                    if opponent != player:
                        if (time.time() - time_hit) >= 5.0:
                            time_hit = time.time()

                            opponent.lives -= 1
                            print(opponent)
                        if opponent.lives == 0:
                            round += 1
                            print("round end")
                            game_state = "round end"
                            player.wins += 1
                block_hit_list = pygame.sprite.spritecollide(player, wall_sprites, False)
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

                if player.is_planter == True and bomb.planting_time > 0:
                    bomb.rect.center = player.rect.center

                elif -0.1 <= bomb.planting_time <= 0.0:
                    time_ticking = time.time()
                    if new_bomb_coords == (-1, -1):
                        new_bomb_coords = player.rect.center
                        bomb.rect.center = new_bomb_coords

                if player.is_planter == False and bomb.planting_time < 1:
                    if pygame.sprite.collide_rect(player, bomb):
                        allow_defuse = True

                if time_ticking != 0.0 and (time.time() - time_ticking) >= 60:
                    player.wins += 1
                    game_state = "round end"
                    time_ticking = 0.0

                if time_defuse > 0 and (time.time() - time_defuse) >= 10 and player.is_planter == False:
                    player.wins += 1
                    game_state = "round end"
                    time_ticking = 0.0
                    time_defuse = 0

        if game_state == "round end":
            if time_round_end == 0.0:
                time_round_end = time.time()
                for player in player_sprites:
                    player.lives = 3
                    player.x_vel = player.y_vel = 0
                planter.rect.topleft = planter_spawn
                defender.rect.topleft = defender_spawn
                bomb.reset()

            elif (time.time() - time_round_end) >= 5:
                game_state = "running"
                time_round_end = 0.0

        elif game_state == "introduction":
            if time_start == 0:
                time_start = time.time()

            if (time.time() - time_start) >= 10:
                game_state = "running"

        # ----------- DRAW THE ENVIRONMENT
        screen.fill(BGCOLOUR)  # fill with bgcolor

        # Draw all sprites
        all_sprites.draw(screen)

        if game_state == "introduction":
            screen.blit(
                font.render("Welcome to Bombfight!", True, BLACK),
                (SCREEN_WIDTH / 3.5, SCREEN_HEIGHT / 3)
            )
            screen.blit(
                font.render("Use WASD/Arrow keys to move.", True, BLACK),
                (SCREEN_WIDTH / 3.5, SCREEN_HEIGHT / 2.5)
            )
            screen.blit(
                font.render("PLANTER: Hold 4 to plant the bomb.", True, BLACK),
                (SCREEN_WIDTH / 16, SCREEN_HEIGHT / 2)
            )

            screen.blit(
                font.render("Hit the defender and", True, BLACK),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.75)
            )

            screen.blit(
                font.render("protect the bomb to win!", True, BLACK),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.65)
            )

            screen.blit(
                font.render("DEFENDER: Hold 4 to defuse the bomb!", True, BLACK),
                (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )

            screen.blit(
                font.render("Attack the planter or!", True, BLACK),
                (SCREEN_WIDTH / 1.65, SCREEN_HEIGHT / 1.75)
            )

            screen.blit(
                font.render("defuse to win!", True, BLACK),
                (SCREEN_WIDTH / 1.65, SCREEN_HEIGHT / 1.65)
            )

        else:
            screen.blit(
                font.render(f"LIVES: {planter.lives}", True, BLACK),
                (SCREEN_WIDTH / 24, SCREEN_HEIGHT / 90)
            )

            screen.blit(font.render(f"LIVES: {planter.lives}", True, BLACK),
                (SCREEN_WIDTH / 24, SCREEN_HEIGHT / 90)
            )

            screen.blit(font.render(f"LIVES: {defender.lives}", True, BLACK),
                (SCREEN_WIDTH / 1.175, SCREEN_HEIGHT / 90)
            )

            screen.blit(font.render(f"LIVES: {defender.lives}", True, BLACK),
                        (SCREEN_WIDTH / 1.175, SCREEN_HEIGHT / 90)
                        )

            screen.blit(font.render(f"{planter.wins} WINS", True, BLACK),
                        (SCREEN_WIDTH / 3.25, SCREEN_HEIGHT / 90)
                        )

            screen.blit(font.render(f"{defender.wins} WINS", True, BLACK),
                        (SCREEN_WIDTH / 1.65, SCREEN_HEIGHT / 90)
                        )

            if time_ticking != 0.0:
                screen.blit(big_font.render(f"{int(60 - (time.time() - time_ticking))}", True, BLACK),
                    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 90)
                )

            if game_state == "round end":
                screen.blit(big_font.render(f"{int(5 - (time.time() - time_round_end))}", True, BLACK),
                            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            )

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()

