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
import pygame_gui
from enum import Enum


class GAMESTATE(Enum):
    """ Used for determining the current state of the game. """
    MENU = 0
    PLAY = 1
    GAMEOVER = 2


class Interface:

    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        """
        Initializes the game interface manager with the required
        objects to display related to the game.
        """
        self.screen = screen
        self.manager = manager
        self._WIDTH = screen.get_width()
        self._HEIGHT = screen.get_height()
        self.state = GAMESTATE.PLAY

        # Create game panel strip at the top of the screen
        self.game_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, -5, self._WIDTH, 50),
            starting_height=1, manager=self.manager, object_id="#game_panel"
        )
        # Create the score label
        score_width = 200
        score_pos_x = self.game_panel.rect.width / 2 - (score_width / 2) - 10
        self.score_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(score_pos_x, 0, score_width, 35),
            text="SCORE: 0", container=self.game_panel
        )

    def update_score(self, score):
        """ Updates the score label with current score of the game. """
        self.score_lbl.set_text(f"SCORE: {score}")
