"""
Game Class - game.py
-----------------------------------------------------------
This class is responsible for handling the game logic,
keyboard and window events, and rendering the game objects.
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
        self.bounderies = pygame.Rect(-Snake.SIZE, 0,
                                      self.WIDTH + Snake.SIZE * 2,
                                      self.HEIGHT + Snake.SIZE)

        # Initialize the game interface manager
        self.interface = Interface(screen, manager)
        # Load the game background
        self.bg = pygame.image.load(Config.assets_path("background.png"))
        # These variables are used in the menu for snake auto path
        self._auto_path_counter = 0
        self._uturn = False
        # Create the Snake object as the player
        self.snake = Snake()
        # Create a starting Food Object (call this after play button event)
        self.apple = None
        # Score of the current game
        self.score = 0

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
            self.interface.update_lifetime(max(0, self.snake.lifetime))

            # Update the snake if it collides with the food and eats it
            self.snake_eat_food_update()

        # Update the movement of the snake
        self.snake.update()
        # Update the snake to loop its movement after hitting the bounderies
        self.snake_loop_bounderies_update()

        # Update the Interface Manager for animation of some elements
        self.interface.update()

    def game_events(self):
        """
        Handles the pygame events (QUIT and keyboard events).
        Returns False for it to signal the game loop to stop.
        Custom events of some game objects are also handled here.
        """
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
                    # Instatiate the apple food
                    self.apple = Food(filename="apple.png", points=10, regen=2)

            # SPAWN FOOD EVENT
            if event.type == Food.SPAWN_FOOD_EVENT:
                self.apple.spawn(off_limits=self.snake.parts)

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        # Draw the background first
        self.screen.blit(self.bg, (0, 0))
        # Draw the game objects
        self.snake.draw(self.screen)

        # Draw game objects that are only viewable in PLAY mode
        if self.state == GAMESTATE.PLAY:
            self.apple.draw(self.screen)

        # Draw the GUI elements from Inteface
        self.interface.draw()

    def snake_menu_auto_path_update(self, time_delta):
        """
        This will randomize the movement of the snake in the menu.
        It must not go over the top and bottom side of window because
        the game panel is currently hidden in the MENU state.
        Every 2 seconds it will randomize a direction of the head.
        """
        xhead, yhead = self.snake.head.bounds.topleft
        direction = self.snake.head.direction
        topmax, botmax = 70, self.HEIGHT - 70
        leftmax, rightmax = 80, self.WIDTH - 80

        if not self._uturn and (yhead < topmax or yhead > botmax):
            self.snake.move(random.choice([Snake.LEFT, Snake.RIGHT]))
            self._auto_path_counter = 0
            self._uturn = True

        if self._auto_path_counter >= 2 and (leftmax < xhead < rightmax):
            # If uturn, then directly change the direction
            if self._uturn:
                movement = Snake.DOWN if yhead < topmax else Snake.UP
                self.snake.move(movement)
                self._uturn = False

            # Remove the current direction and its opposite direction
            moves = [Snake.UP, Snake.DOWN, Snake.LEFT, Snake.RIGHT]
            to_remove = [direction, direction * -1]
            moves = [move for move in moves if move not in to_remove]

            # Randomize the next valid moves
            next_move = random.choice(moves)
            self.snake.move(next_move)
            self._auto_path_counter = 0

        self._auto_path_counter += time_delta

    def snake_loop_bounderies_update(self):
        """
        Check if each snake part collides with window bounderies
        If it collides then the part should appear on the opposite side.
        """
        snake_parts = self.snake.parts
        for part in snake_parts:
            if part.bounds.clamp(self.bounderies) != part.bounds:
                bounds = part.bounds.topleft + pygame.Vector2(Snake.SIZE)
                x = (bounds.x % (self.WIDTH + Snake.SIZE)) - Snake.SIZE
                y = ((bounds.y - Snake.SIZE) % self.HEIGHT)
                part.teleport(x, y)

    def snake_eat_food_update(self):
        """
        Checks if the snake head collides with the current food.
        If it collides then destroy the food and grow the snake.
        """
        if self.apple.spawned:
            if self.snake.head.bounds.colliderect(self.apple.bounds):
                # Spawn a regen label
                apple_pos = pygame.Vector2(self.apple.bounds.topleft)
                self.interface.spawn_regen_label(apple_pos, self.apple.regen)
                # Update the score add the health regen
                self.score += self.apple.points
                self.snake.lifetime += self.apple.regen
                # Update the game labels
                self.interface.update_score(self.score)
                self.interface.update_stretch(self.snake.stretch)
                # Destroy the apple and grow the snake
                self.snake.grow()
                self.apple.destroy()
