# BOMBLORANT
# Author: Samantha J
# 2022 Version

# This game is inspired by VALORANT by Riot Games

# Credit to Epidemic Sound for the sound effects
# https://www.epidemicsound.com/
# Background and bomb graphics taken from Freepik
# Credit to Simpson College for the base player movement and collision code
#
# TODO: Credit code I took inspiration from/used as a base
# TODO: Change project name to Bomblorant

import time
import pygame
from pygame import mixer

pygame.init()

pygame.mixer.init()

# Constants
BOMB_TICKING_SOUND = pygame.mixer.Sound("./Music/ES_Bomb Timer 4 - SFX Producer.mp3")
ROUND_END_SOUND = pygame.mixer.Sound("./Music/ES_Game Chime Winner - SFX Producer.mp3")
HIT_SOUND = pygame.mixer.Sound("./Music/ES_Impact Brick Hit 2 - SFX Producer.mp3")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOUR = (100, 100, 255)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "BOMBLORANT"


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
        is_planter: determines whether the player is the bomb planter
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
    planting_period: how much time is left until the bomb is planted
    plant_speed: the speed that the planting_period decreases at
    """

    def __init__(self, coords: tuple) -> None:
        """
        Arguments:
            coords: tuple of (x,y) to represent location
        """

        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load("./images/bomb.png"),
            (20, 20)
        )

        self.rect = self.image.get_rect()

        self.planting_period = 15.0
        self.plant_speed = 0.0

    def update(self):
        """ Updates how much time is left until the bomb is planted"""
        self.planting_period -= self.plant_speed

    def reset(self):
        " Resets the planting period"

        self.planting_period = 15.0

    def plant(self):
        """ Increases the plant speed"""
        self.plant_speed = 0.1

    def stop_plant(self):
        """ Sets the plant speed to 0"""
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

    new_bomb_coords = (-1, -1)
    time_ticking = 0.0
    time_defuse = 0

    game_state = "introduction"

    planter_click = False  # Prevents player one from holding down more than one key
    defender_click = False  # Prevents player one from holding down more than one key
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

    # Initialize sprites
    planter = Player(planter_spawn, RED)
    planter.is_planter = True
    defender = Player(defender_spawn, BLUE)
    all_sprites.add(planter)
    all_sprites.add(defender)
    player_sprites.add(planter)
    player_sprites.add(defender)
    time_hit = 0.0
    time_until_explosion = 60
    time_round_end = 0.0
    time_start = 0
    time_between_rounds = 5
    round = 1

    bomb = Bomb(planter.rect.center)
    all_sprites.add(bomb)

    for attribute in wall_attributes:
        wall = Wall(*attribute)

        wall_sprites.add(wall)
        all_sprites.add(wall)

    font = pygame.font.SysFont("Arial", 25)
    big_font = pygame.font.SysFont("Arial", 40)

    # ----------- MAIN LOOP
    while not done:
        # ----------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # If the game is currently running a round, allow player movement through keys
            if game_state == "running":

                if event.type == pygame.KEYDOWN:
                    # If the key pressed is one of the planter's keys and the planter
                    # is not already holding down another key
                    if event.key in planter_keys and planter_click == False:
                        # Stop the planter's current movement to prevent multiple actions
                        planter.stop()

                        # Record that the planter is holding a key down
                        planter_click = True

                        # Check which key is pressed and update the planter accordingly
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

                    # If the key pressed is one of the defender's keys and the defender
                    # is not already holding down another key
                    elif event.key in defender_keys and defender_click == False:
                        # Stop the defender's current movement to prevent multiple actions
                        defender.stop()

                        # Record that the defender is holding a key down
                        defender_click = True

                        # Check which key is pressed and update the planter accordingly
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
                    if event.key in planter_keys:

                        # Record that the planter has released hold on a key
                        planter_click = False

                        # stop planter movement
                        if planter.x_vel != 0 or planter.y_vel != 0:
                            planter.stop()

                        if event.key == pygame.K_4:
                            # if the planter is planting the bomb and hasn't finished,
                            # stop the bomb from planting
                            bomb.stop_plant()

                    elif event.key in defender_keys:

                        # Record that the defender has released hold on a key
                        defender_click = False

                        # stop planter movement
                        if defender.x_vel != 0 or defender.y_vel != 0:
                            defender.stop()

                        if event.key == pygame.K_KP4:
                            # if the planter is defusing the bomb and hasn't finished,
                            # Reset the defusing time
                            time_defuse = 0

        # ----------- CHANGE ENVIRONMENT

        all_sprites.update()

        if game_state == "running":
            for player in player_sprites:

                # If the player reaches either side of the tunnel on the map,
                # teleport the player to the other side
                if 354 < player.rect.y <= player.rect.y <= 414:
                    if player.rect.right <= 0:
                        player.rect.left = SCREEN_WIDTH
                    elif player.rect.left >= SCREEN_WIDTH:
                        player.rect.right = 0

                # See if the player hit the opponent
                opponent_hit = pygame.sprite.spritecollide(player, player_sprites, False)
                for opponent in opponent_hit:
                    # Check that the opponent isn't the player
                    if opponent != player:
                        # if the player hit the opponent past the cooldown,
                        if (time.time() - time_hit) >= time_invincible:
                            pygame.mixer.Channel(1).play(HIT_SOUND)

                            time_hit = time.time()

                            # Take one of the opponent's lives
                            opponent.lives -= 1

                            # Reset the opponent's location depending on role
                            if opponent.is_planter == True:
                                opponent.rect.topleft = planter_spawn
                            else:
                                opponent.rect.topleft = defender_spawn

                        if opponent.lives == 0:
                            # if the opponent has no more lives left, the round ends
                            game_state = "round end"
                            player.wins += 1

                # See if the player hits a wall
                wall_hit_list = pygame.sprite.spritecollide(player, wall_sprites, False)
                for wall in wall_hit_list:
                    if player.x_vel > 0 and wall.rect.left <= player.rect.right < wall.rect.right:
                        # If the player is moving right and the player is not within the width region of the wall,
                        # Set their right side to the left side of the block hit
                        player.stop()
                        player.rect.right = wall.rect.left
                    elif player.x_vel < 0 and wall.rect.right >= player.rect.left > wall.rect.left:
                        # If the player is moving left and the player is not within the width region of the wall,
                        # do the opposite
                        player.stop()
                        player.rect.left = wall.rect.right

                    elif player.y_vel > 0 and wall.rect.top <= player.rect.bottom < wall.rect.bottom:
                        # If the player is moving down and the player is not within the height region of the wall,
                        # Set their bottom side to the top of the block hit
                        player.stop()
                        player.rect.bottom = wall.rect.top
                    elif player.y_vel < 0 and wall.rect.bottom >= player.rect.top > wall.rect.top:
                        # if the player is moving up and the player is not within the height region of the wall,
                        # Do the opposite
                        player.stop()
                        player.rect.top = wall.rect.bottom

                if player.is_planter == True:
                    if bomb.planting_period > 0:
                        # If the planter has not yet planted the bomb, keep the bomb on the player
                        bomb.rect.center = player.rect.center

                    if -0.1 <= bomb.planting_period <= 0.0:
                        # When the player plants the bomb, begin the bomb ticking time
                        time_ticking = time.time()

                        # Keep the bomb at the planted location
                        new_bomb_coords = player.rect.center
                        bomb.rect.center = new_bomb_coords

                if player.is_planter == False and bomb.planting_period < 1:
                    # if the player is not the planter and the bomb has been planted,
                    if pygame.sprite.collide_rect(player, bomb):
                        # allow the player to defuse the bomb
                        allow_defuse = True

            if time_ticking != 0.0:
                # if the time ticking until the bomb expodes has been set (happens when the bomb is planted)
                if time_ticking == time.time():
                    # start the bomb ticking sound
                    pygame.mixer.Channel(0).play(BOMB_TICKING_SOUND, -1)

                if (time.time() - time_ticking) >= time_until_explosion:
                    # if it is time for the bomb to explode, the planter wins
                    player.wins += 1

                    # end the round
                    game_state = "round end"

                    # reset the bomb ticking time
                    time_ticking = 0.0

            if time_defuse > 0 and (time.time() - time_defuse) >= 10:
                # if the defender successfully defuses the bomb before the time runs out,
                # the defender wins the round
                defender.wins += 1

                # end the round
                game_state = "round end"

        if game_state == "round end":
            # if the round has ended
            if time_round_end == 0.0:
                # Stop current sounds and play the round end sound
                pygame.mixer.stop()
                pygame.mixer.Channel(0).play(ROUND_END_SOUND)

                # Reset attributes and values
                for player in player_sprites:
                    player.lives = 3
                    player.x_vel = player.y_vel = 0

                time_round_end = time.time()
                time_ticking = 0.0
                time_defuse = 0

                round += 1

                bomb.reset()

                # Return players to spawnpoints
                planter.rect.topleft = planter_spawn
                defender.rect.topleft = defender_spawn

            elif (time.time() - time_round_end) >= time_between_rounds:
                # If it has been more than the set time between rounds,
                # start the next round
                game_state = "running"

                # reset the time that the round ended
                time_round_end = 0.0

        elif game_state == "introduction":
            # if the time started has not been set to the current time,
            if time_start == 0:
                # set the time started to the current time
                time_start = time.time()

            # if the introduction time has passed, start the game
            if (time.time() - time_start) >= time_introduction:
                game_state = "running"

        # ----------- DRAW THE ENVIRONMENT
        screen.fill(BGCOLOUR)  # fill with bgcolor

        # Draw all sprites
        all_sprites.draw(screen)

        if game_state == "introduction":
            # Show introductory messages
            screen.blit(
                big_font.render(f"Welcome to {WINDOW_TITLE}!", True, BLACK),
                (SCREEN_WIDTH / 3.5, SCREEN_HEIGHT / 4)
            )
            screen.blit(
                big_font.render("Use WASD/Arrow keys to move.", True, BLACK),
                (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3)
            )
            screen.blit(
                big_font.render("PLANTER", True, RED),
                (SCREEN_WIDTH / 6.5, SCREEN_HEIGHT / 2.10)
            )

            screen.blit(
                font.render("Hold 4 to plant the bomb.", True, WHITE),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.85)
            )

            screen.blit(
                font.render("Hit the defender and", True, WHITE),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.70)
            )

            screen.blit(
                font.render("protect the bomb until", True, WHITE),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.57)
            )

            screen.blit(
                font.render("the time runs out to win!", True, WHITE),
                (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.45)
            )

            screen.blit(
                big_font.render("DEFENDER", True, BLUE),
                (SCREEN_WIDTH / 1.65, SCREEN_HEIGHT / 2.10)
            )

            screen.blit(
                font.render("Hold 4 on the bomb for", True, WHITE),
                (SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 1.85)
            )

            screen.blit(
                font.render("10 seconds to defuse it!", True, WHITE),
                (SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 1.70)
            )

            screen.blit(
                font.render("Hit the planter or", True, WHITE),
                (SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 1.57)
            )

            screen.blit(
                font.render("defuse before the", True, WHITE),
                (SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 1.47)
            )

            screen.blit(
                font.render("bomb explodes to win!", True, WHITE),
                (SCREEN_WIDTH / 1.75, SCREEN_HEIGHT / 1.37)
            )

        else:
            # Else, show player lives and wins
            screen.blit(
                font.render(f"LIVES: {planter.lives}", True, RED),
                (SCREEN_WIDTH / 24, SCREEN_HEIGHT / 90)
            )

            screen.blit(font.render(f"LIVES: {defender.lives}", True, BLUE),
                        (SCREEN_WIDTH / 1.175, SCREEN_HEIGHT / 90)
                        )

            screen.blit(font.render(f"{planter.wins} WINS", True, RED),
                        (SCREEN_WIDTH / 3.25, SCREEN_HEIGHT / 90)
                        )

            screen.blit(font.render(f"{defender.wins} WINS", True, BLUE),
                        (SCREEN_WIDTH / 1.65, SCREEN_HEIGHT / 90)
                        )

            if time_ticking != 0.0:
                # if the bomb has been planted, show the time left until the bomb explored
                screen.blit(big_font.render(f"{int(time_until_explosion - (time.time() - time_ticking))}", True, WHITE),
                            (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 90)
                            )

            if game_state == "round end":
                # if the round has ended,

                # show the time left until the next round
                screen.blit(
                    big_font.render(f"{int(time_between_rounds - (time.time() - time_round_end))}", True, BLACK),
                    (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.75)
                    )

                # show the round number
                screen.blit(big_font.render(f"ROUND {round}", True, WHITE),
                            (SCREEN_WIDTH / 2.25, SCREEN_HEIGHT / 2)
                            )

        # Update the screen
        pygame.display.flip()

        # ----------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()


