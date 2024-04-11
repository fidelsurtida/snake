"""
Interface Class - interface.py
-----------------------------------------------------------
This module contains the Interface Class that is responsible
for initializing game elements like lables, buttons and
panels that will be used and displayed by the GUI Manager.
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
        self.state = GAMESTATE.PLAY
        self._WIDTH = screen.get_width()
        self._HEIGHT = screen.get_height()

        # Initialize all the GUI elements for PLAY state
        self._initialize_play_elements()
        # Container for tracking the regen labels for animation
        self._regen_labels = []

    def _initialize_play_elements(self):
        """
        Creates the GUI for the PLAY state of the game.
        """
        score_width = 200
        lifetime_width = 200
        stretch_width = 180

        # Create game panel strip at the top of the screen
        self.game_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, -5, self._WIDTH, 50),
            starting_height=1, manager=self.manager, object_id="#game_panel"
        )
        # Create the score label
        score_pos_x = self.game_panel.rect.center[0] - (score_width / 2) - 10
        self._score_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(score_pos_x, 0, score_width, 35),
            text="SCORE: 0", container=self.game_panel, object_id="#score_lbl"
        )
        # Create the lifetime label
        self._lifetime_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(20, 0, lifetime_width, 35),
            text="LIFETIME: 100", container=self.game_panel,
            object_id="#lifetime_lbl"
        )
        # Create the stretch label (length of the snake)
        stretch_pos_x = self.game_panel.rect.width - stretch_width
        self._stretch_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(stretch_pos_x, 0, stretch_width, 35),
            text="STRETCH: 0m", container=self.game_panel,
            object_id="#stretch_lbl"
        )

    def update(self):
        """ Updates manually some of the animations for GUI elements. """
        for label in self._regen_labels:
            x, y = label.rect.topleft
            label.set_relative_position((x, y-1))

    def process_events(self, event):
        """ Checks for events related to pygame_gui elements."""
        # TEXT EFFECT FINISHED EVENT
        if event.type == pygame_gui.UI_TEXT_EFFECT_FINISHED:
            if event.ui_element.get_object_id() == "@regen_lbl":
                self._regen_labels.remove(event.ui_element)
                event.ui_element.kill()

    def spawn_regen_label(self, position, regen):
        """ Spawns a label that shows the regen stat after eating food. """
        hp_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(position.x, position.y-30, 60, 40),
            text=f"+{regen}♥", object_id="@regen_lbl"
        )
        self._regen_labels.append(hp_label)
        hp_label.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT,
                                   {"time_per_alpha_change": 6})

    def update_score(self, score):
        """ Updates the score label with current score of the game. """
        self._score_lbl.set_text(f"SCORE: {score}")

    def update_lifetime(self, lifetime):
        """ Updates the lifetime label with current lifetime of the game. """
        self._lifetime_lbl.set_text(f"LIFETIME: {lifetime:.1f}")

    def update_stretch(self, stretch):
        """ Updates the stretch label with current length of the snake. """
        self._stretch_lbl.set_text(f"STRETCH: {stretch}m")
