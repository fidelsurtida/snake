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
import pygame_gui
from src.config import Config
from src.game import Game


# Initialize Pygame
pygame.init()

# Create the Screen and GUI Manager
screen = pygame.display.set_mode(Config.SCREEN_DIMENSIONS)
manager = pygame_gui.UIManager(Config.SCREEN_DIMENSIONS, Config.theme_path())
pygame.display.set_caption("Snake Game")


def main():

    # Create instance of the Game class and include also the GUI manager
    game = Game(screen, manager)
    # Create the game clock object for limiting the FPS
    clock = pygame.time.Clock()

    # Game Loop
    running = True
    while running:
        # Limit FPS to 60 and get time delta
        time_delta = clock.tick(60)

        # Event handling
        running = game.game_events()

        # Game and GUI Updates
        game.update(time_delta / 1000)
        manager.update(time_delta)

        # Clear the screen
        screen.fill("black")

        # Render the Game Objects and the GUI
        game.draw()
        manager.draw_ui(screen)

        # Update the screen
        pygame.display.flip()

    # Quit Pygame after the game loop ends
    pygame.quit()


if __name__ == "__main__":
    main()
