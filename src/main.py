"""
SNAKE GAME
-------------------------------------
A simple snake game using Pygame.
Based on the classic Nokia Snake game.
-------------------------------------
Author: Fidel Jesus O. Surtida I
Project Start: March 27, 2024
-------------------------------------
"""
import pygame
from src.game import Game


# Initialize Pygame
pygame.init()

# Set up the screen size, window title and game clock
SCREEN_WIDTH, SCREEN_HEIGHT = (1024, 768)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")


def main():
    # Create instance of the Game class
    game = Game(screen)

    # Game Loop
    running = True
    while running:
        # Event handling
        running = game.game_events()

        # Game Updates
        game.update()

        # Clear the screen
        screen.fill("black")

        # Render the Game Objects
        game.draw()

        # Update the screen
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Quit Pygame after the game loop ends
    pygame.quit()


if __name__ == "__main__":
    main()
