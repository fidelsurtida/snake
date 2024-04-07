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
from interface import Interface
from objects.snake import SIZE as SNAKESIZE
from objects.snake import Snake
from objects.food import Food


class Game:
    def __init__(self, screen: pygame.Surface):
        """
        Initialization of game objects and parameters.
        """
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.screen = screen
        self.bounderies = pygame.Rect(-SNAKESIZE, -SNAKESIZE,
                                      self.WIDTH + SNAKESIZE * 2,
                                      self.HEIGHT + SNAKESIZE * 2)

        # Initialize the game interface manager
        self.interface = Interface(screen)
        # Create the Snake object as the player
        self.snake = Snake()
        # Create a starting Food Object
        self.apple = Food(screen_width=self.WIDTH, screen_height=self.HEIGHT)
        # Score of the current game
        self.score = 0

    def update(self):
        """
        Handles the game logic. Updates the game objects and status.
        """
        # Update the movement of the snake
        self.snake.update()
        # Update the snake to loop its movement after hitting the bounderies
        self.snake_loop_bounderies_update()
        # Update the snake if it collides with the food and eats it
        self.snake_eat_food_update()

    def game_events(self):
        """
        Handles the pygame events (QUIT and keyboard events).
        Returns False for it to signal the game loop to stop.
        Custom events of some game objects are also handled here.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # KEYBOARD EVENTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.snake.move(Snake.LEFT)
                if event.key == pygame.K_d:
                    self.snake.move(Snake.RIGHT)
                if event.key == pygame.K_w:
                    self.snake.move(Snake.UP)
                if event.key == pygame.K_s:
                    self.snake.move(Snake.DOWN)

            # SPAWN FOOD EVENT
            if event.type == Food.SPAWN_FOOD_EVENT:
                self.apple.spawn()

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)

        # Lastly draw the game interface
        self.interface.draw()

    def snake_loop_bounderies_update(self):
        """
        Check if each snake part collides with window bounderies
        If it collides then the part should appear on the opposite side.
        """
        snake_parts = self.snake.parts
        for part in snake_parts:
            if part.bounds.clamp(self.bounderies) != part.bounds:
                bounds = part.bounds.topleft + pygame.Vector2(SNAKESIZE)
                x = (bounds.x % (self.WIDTH + SNAKESIZE)) - SNAKESIZE
                y = (bounds.y % (self.HEIGHT + SNAKESIZE)) - SNAKESIZE
                part.teleport(x, y)

    def snake_eat_food_update(self):
        """
        Checks if the snake head collides with the current food.
        If it collides then destroy the food and grow the snake.
        """
        if self.apple.spawned:
            if self.snake.head.bounds.colliderect(self.apple.bounds):
                self.apple.destroy()
                self.snake.grow()
                # Update the score and the label
                self.score += 10
                self.interface.update_score(self.score)
