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
from objects.snake import Snake


class Game:
    def __init__(self, screen: pygame.Surface):
        """
        Initialization of game objects and parameters.
        """
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.screen = screen

        # Create the Snake object as the player
        self.snake = Snake()

    def update(self):
        """
        Handles the game logic. Updates the game objects and status.
        """
        self.snake.update()

    def game_events(self):
        """
        Handles the pygame events (QUIT and keyboard events).
        Returns False for it to signal the game loop to stop.
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

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        self.snake.draw(self.screen)
