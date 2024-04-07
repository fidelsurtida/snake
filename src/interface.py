"""
Interface Class - interface.py
-----------------------------------------------------------
This module contains the Interface Class tha is responsible
for displaying required game labels and sprites on the
screen depending on the current state of the game.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
from enum import Enum


class GAMESTATE(Enum):
    """ Used for determining the current state of the game. """
    MENU = 0
    PLAY = 1
    GAMEOVER = 2


class Interface:

    def __init__(self, screen: pygame.Surface):
        """
        Initializes the game interface manager with the required
        objects to display related to the game.
        """
        self.screen = screen
        self._WIDTH = screen.get_width()
        self._HEIGHT = screen.get_height()
        self.state = GAMESTATE.PLAY

        # Create the game font and labels
        self.font = pygame.font.SysFont("stheitimedium", 20)
        self._score_lbl = self.font.render(f"SCORE: {0:>5}", True, "white")

    def draw(self):
        """
        Draws the required interface depending on the
        current state of the game.
        """
        match self.state:
            case GAMESTATE.PLAY:
                x_pos = self._WIDTH / 2 - (self._score_lbl.get_width() / 2)
                self.screen.blit(self._score_lbl, (x_pos, 15))

    def update_score(self, score):
        """ Updates the score label with current score of the game. """
        self._score_lbl = self.font.render(f"SCORE: {score:>5}", True, "white")
