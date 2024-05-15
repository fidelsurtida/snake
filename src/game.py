"""
Game Class - game.py
-----------------------------------------------------------
This class is responsible for handling the game logic,
keyboard and window events, and rendering the game objects.
This handles the main logic decisions of the game and
calls object methods accordingly.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
import pygame_gui
import random
from interface import Interface
from src.config import Config
from src.config import GAMESTATE
from src.objects.snake import Snake
from src.objects.food import Food
from src.objects.foodbuff import FoodBuff
from src.objects.speedup import SpeedUp
from src.objects.slowdown import SlowDown


class Game:

    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        """
        Initialization of game objects and parameters.
        """
        self.HEIGHT = Config.SCREEN_HEIGHT
        self.WIDTH = Config.SCREEN_WIDTH
        self.screen = screen
        self.manager = manager
        self.state = GAMESTATE.MENU
        self.bounderies = pygame.Rect(10, 10, self.WIDTH - 20, self.HEIGHT - 20)

        # Initialize the game interface manager
        self.interface = Interface(screen, manager)
        # Load the game background and the panel image
        self._load_game_backgrounds()
        # These variables are used for various flags regarding the snake
        self._auto_path_counter = 0
        self._gameover_counter = 0.12
        self._uturn = None
        # Create the Snake object as the player and pass the game background
        self.snake = Snake(background=self.bgwalled)
        # Create a starting Food Object (creation at play button press)
        self.apple = None
        self.golden_apple = None
        # Create the starting item buffs (creation at play button press)
        self.speedup = None
        # Create the debuff items (creation at play button press)
        self.slowdown = None
        # Score and total time of the current game
        self.score = 0
        self.total_time = 0

    def _load_game_backgrounds(self):
        """ Loads the background image and the walls on each window. """
        self.bg = pygame.image.load(Config.assets_path("background.png"))
        panel = pygame.image.load(Config.assets_path("panel.png"))
        # Get only a part of the panel background to make as a wall
        self.wall_top = panel.subsurface(0, 25, 994, 25)
        self.wall_bottom = pygame.transform.rotate(self.wall_top, 180)
        self.wall_left = pygame.transform.rotate(self.wall_top, 90)
        self.wall_right = pygame.transform.rotate(self.wall_top, -90)
        # Create a walled background for the snake
        self.bgwalled = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.bgwalled.blit(self.bg, (0, 0))
        self.bgwalled.blit(self.wall_left, (0, 0))
        self.bgwalled.blit(self.wall_right, (self.WIDTH - 25, 0))
        self.bgwalled.blit(self.wall_top, (15, 0))
        self.bgwalled.blit(self.wall_bottom, (15, self.HEIGHT - 25))

    def reset_game(self):
        """
        This will be called in events to reset the game state to new game.
        All variables that needs to return to initial value should be put here.
        """
        self.snake = Snake(background=self.bgwalled)
        self._gameover_counter = 0.12
        self._auto_path_counter = 0
        self._uturn = False
        self.score = 0
        self.total_time = 0

    def update(self, time_delta):
        """
        Handles the game logic. Updates the game objects and status.
        This also is passed the time_delta computation from the main loop.
        """
        # HANDLE MENU UPDATES
        if self.state == GAMESTATE.MENU:
            # Update the snake for the menu auto path
            self.snake_menu_auto_path_update(time_delta)

        # HANDLE PLAY UPDATES
        elif self.state == GAMESTATE.PLAY:
            # Reduce the life of the player based on the passed time
            self.snake.lifetime -= time_delta
            self.total_time += time_delta
            self.interface.update_lifetime(max(0, self.snake.lifetime))

            # Update the snake if it collides with the food and eats it
            self.snake_eat_food_update(self.apple)
            self.snake_eat_food_update(self.golden_apple)

            # Update the snake if it collides with the items and eats it
            self.snake_eat_items_update(self.speedup)
            self.snake_eat_items_update(self.slowdown)

            # Update the food objects for its animation states
            self.apple.update(time_delta)
            self.golden_apple.update(time_delta)

            # Check if the snake head collides with its body parts
            self.snake_collide_self_checker(time_delta)
            # Check if the snake collides with the window bounderies
            self.snake_bump_bounderies_update()

            # Update the buff items for animation states
            self.speedup.update(time_delta)
            # Update the debuff items for animation states
            self.slowdown.update(time_delta)

        # UPDATE MOVEMENT OF SNAKE IN MENU AND PLAY STATES
        if self.state == GAMESTATE.MENU or self.state == GAMESTATE.PLAY:
            # Update the movement of the snake
            self.snake.update(time_delta)

        # Update the Interface Manager for animation of some elements
        self.interface.update()

    def game_events(self):
        """
        Handles the pygame events (QUIT and keyboard events).
        Returns False for it to signal the game loop to stop.
        Custom events of some game objects are also handled here.
        """
        # HELPER FUNCTIONS FOR THE GAME EVENTS
        def instantiate_foods():
            self.apple = Food(filename="apple.png", points=10, regen=2)
            self.golden_apple = FoodBuff(filename="goldapple.png",
                                         points=50, regen=5)

        def instantiate_items():
            self.speedup = SpeedUp(name="speedup", filename="speedup.png",
                                   points=20, value=5, negative=False)
            self.slowdown = SlowDown(name="slowdown", filename="snail.png",
                                     points=10, value=2, negative=True)

        def all_territories():
            return ([self.apple.territory, self.golden_apple.territory,
                    self.speedup.territory, self.slowdown.territory] +
                    self.snake.rects)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # GUI Manager pass each event to the pygame_gui
            self.manager.process_events(event)
            # Pass the event also to the interface manager
            self.interface.process_events(event)

            # PLAY KEYBOARD EVENTS
            if self.state == GAMESTATE.PLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.snake.move(Snake.LEFT)
                    if event.key == pygame.K_d:
                        self.snake.move(Snake.RIGHT)
                    if event.key == pygame.K_w:
                        self.snake.move(Snake.UP)
                    if event.key == pygame.K_s:
                        self.snake.move(Snake.DOWN)

            # GUI BUTTON EVENTS
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # START BUTTON EVENT
                if event.ui_element == self.interface.start_btn:
                    self.state = GAMESTATE.PLAY
                    self.interface.start_game_event()
                    # Instatiate the apple food and golden apple
                    instantiate_foods()
                    # Instantiate also the buff items
                    instantiate_items()

                # RESTART BUTTON EVENT
                elif event.ui_element == self.interface.restart_btn:
                    self.state = GAMESTATE.PLAY
                    self.interface.restart_game_event()
                    self.reset_game()
                    # Reset the food objects
                    instantiate_foods()
                    # Reset the buff items
                    instantiate_items()

                # QUIT BUTTON EVENT
                elif event.ui_element == self.interface.quit_btn:
                    self.state = GAMESTATE.MENU
                    self.interface.main_menu_event()
                    self.reset_game()

            # SPAWN FOOD EVENT
            if self.state == GAMESTATE.PLAY:
                if event.type == Food.SPAWN_FOOD_EVENT:
                    self.apple.spawn(off_limits_rects=all_territories())
                if event.type == FoodBuff.SPAWN_FOOD_BUFF_EVENT:
                    self.golden_apple.spawn(off_limits_rects=all_territories())

            # SPAWN ITEMS EVENT
            if self.state == GAMESTATE.PLAY:
                if event.type == SpeedUp.SPAWN_SPEED_UP_EVENT:
                    self.speedup.spawn(off_limits_rects=all_territories())
                if event.type == SlowDown.SPAWN_SLOW_DOWN_EVENT:
                    territory = all_territories()
                    self.slowdown.spawn_near_head(head=self.snake.head,
                                                  off_limits_rects=territory)

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        # Draw the background first
        self.screen.blit(self.bg, (0, 0))
        # Draw the walls on every boundery of the screen
        self.screen.blit(self.wall_left, (0, 0))
        self.screen.blit(self.wall_right, (self.WIDTH - 25, 0))
        self.screen.blit(self.wall_top, (15, 0))
        self.screen.blit(self.wall_bottom, (15, self.HEIGHT - 25))

        # Draw the game objects
        self.snake.draw(self.screen)
        # Draw game objects that are only viewable in PLAY mode
        if self.state == GAMESTATE.PLAY:
            self.apple.draw(self.screen)
            self.golden_apple.draw(self.screen)
            self.speedup.draw(self.screen)
            self.slowdown.draw(self.screen)

        # Draw the GUI elements from Inteface
        self.interface.draw()

    def snake_menu_auto_path_update(self, time_delta):
        """
        This will randomize the movement of the snake in the menu.
        It must not go over the bounderies of the window
        Every second it will randomize a direction of the head.
        """
        xhead, yhead = self.snake.head.bounds.topleft
        direction = self.snake.head.direction
        topmax, botmax = 60, self.HEIGHT - 100
        leftmax, rightmax = 60, self.WIDTH - 100

        if not self._uturn and (yhead < topmax or yhead > botmax):
            self.snake.move(random.choice([Snake.LEFT, Snake.RIGHT]))
            self._auto_path_counter = 0.6
            self._uturn = [Snake.DOWN] if yhead < topmax else [Snake.UP]

        if not self._uturn and (xhead < leftmax or xhead > rightmax):
            self.snake.move(random.choice([Snake.UP, Snake.DOWN]))
            self._auto_path_counter = 0.6
            self._uturn = [Snake.RIGHT] if xhead < leftmax else [Snake.LEFT]

        if self._auto_path_counter >= 1:
            # Remove the current direction and its opposite direction
            moves = [Snake.UP, Snake.DOWN, Snake.LEFT, Snake.RIGHT]
            if self._uturn:
                moves = self._uturn
            else:
                to_remove = [direction, direction * -1]
                moves = [move for move in moves if move not in to_remove]

            # Randomize the next valid moves
            next_move = random.choice(moves)
            self.snake.move(next_move)
            self._auto_path_counter = -1 if self._uturn else 0
            self._uturn = None

        self._auto_path_counter += time_delta

    def snake_eat_food_update(self, food):
        """
        Checks if the snake head collides with the specified food.
        If it collides then destroy the food and grow the snake.
        """
        if food.spawned:
            if self.snake.head.bounds.colliderect(food.bounds):
                # Spawn a regen label
                apple_pos = pygame.Vector2(food.bounds.topleft)
                self.interface.spawn_regen_label(apple_pos, food.regen,
                                                 food.points)
                # Update the score add the health regen
                self.score += food.points
                self.snake.lifetime += food.regen
                # Update the game labels
                self.interface.update_score(self.score)
                self.interface.update_stretch(self.snake.stretch)
                # Destroy the apple and grow the snake
                self.snake.grow()
                food.destroy()

    def snake_eat_items_update(self, item):
        """
        Checks if the snake head collides with the specified item.
        If it collides determine the type of item and apply the
        buff into the snake object.
        """
        if item.spawned:
            if self.snake.head.bounds.colliderect(item.bounds):
                # Display a buff icon and points floater
                item_pos = pygame.Vector2(item.bounds.topleft)
                self.interface.spawn_buff_label(buff_icon=item.image.copy(),
                                                position=item_pos,
                                                buff_value=item.value,
                                                points=item.points,
                                                negate=item.negative)
                # Apply the buff item to the snake head
                self.snake.apply_buff(item)
                # Add the score and update the game labels
                self.score += item.points
                self.interface.update_score(self.score)
                # Destroy the item
                item.destroy()

    def snake_bump_bounderies_update(self):
        """
        Check if each head part collides with window bounderies
        If it collides then the snake is dead, and it's game over.
        Set the game over counter to 0, the code to trigger the whole
        game over event is found in the snake_collide_self_checker.
        """
        snake_head = self.snake.head
        if snake_head.bounds.clamp(self.bounderies) != snake_head.bounds:
            self._gameover_counter = 0

    def snake_collide_self_checker(self, time_delta):
        """
        Checks if the head part collides with any of the moving snake parts.
        If the condition is true, reduce the gameover counter delay in order
        for the snake to collide with its body.
        """
        for body in self.snake.body[1:]:
            if self.snake.head.bounds.colliderect(body.bounds):
                self._gameover_counter -= time_delta
                break

        # If the gameover counter reaches zero, then set state to GAMEOVER
        # We also need to compute the death moment location of the snake
        # And finally pass the final game data to the results panel
        if self._gameover_counter <= 0:
            # Set the game state to GAMEOVER
            self.state = GAMESTATE.GAMEOVER
            self.interface.gameover_event()

            # Set the dead image sprite of the snake head
            self.snake.die()
            self.snake.draw(self.screen)

            # Set the moments image of the snake in the gameover screen
            width, height, (x, y) = 320, 180, self.snake.head.bounds.topleft
            snakepos = (x - (width // 3) - 20, y - (height // 3))
            moments_rect = pygame.Rect(*snakepos, width, height)
            moments_rect = moments_rect.clamp(self.screen.get_rect())
            moments = self.screen.subsurface(moments_rect)
            self.interface.update_moments_image(moments)

            # Pass the final game data to the results panel
            self.interface.update_results_data(score=self.score,
                                               stretch=self.snake.stretch,
                                               lifetime=self.total_time)
