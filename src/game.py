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


class Game:
    def __init__(self, screen: pygame.Surface):
        """
        Initialization of game objects and parameters.
        """
        self.HEIGHT = screen.get_height()
        self.WIDTH = screen.get_width()
        self.screen = screen

        # Sample rectangle player
        self.SNAKE_SPEED = 5
        self.player = pygame.Rect(self.WIDTH // 2, self.HEIGHT // 2, 50, 50)
        self.velocity = pygame.Vector2(self.SNAKE_SPEED, 0)

    def update(self):
        """
        Handles the game logic. Updates the game objects and status.
        """
        self.player.move_ip(self.velocity.x, self.velocity.y)
        if self.player.clamp(self.screen.get_rect()) != self.player:
            self.velocity = pygame.Vector2(0, 0)

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
                    self.velocity = pygame.Vector2(-self.SNAKE_SPEED, 0)
                if event.key == pygame.K_d:
                    self.velocity = pygame.Vector2(self.SNAKE_SPEED, 0)
                if event.key == pygame.K_w:
                    self.velocity = pygame.Vector2(0, -self.SNAKE_SPEED)
                if event.key == pygame.K_s:
                    self.velocity = pygame.Vector2(0, self.SNAKE_SPEED)

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        pygame.draw.rect(self.screen, "white", self.player)
