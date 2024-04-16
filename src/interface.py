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
from src.config import Config
from src.config import GAMESTATE
from src.objects.floater import Floater


class Interface:

    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        """
        Initializes the game interface manager with the required
        objects to display related to the game.
        """
        self.screen = screen
        self.manager = manager
        self.state = GAMESTATE.MENU
        self._WIDTH = screen.get_width()
        self._HEIGHT = screen.get_height()

        # Load first the icons image for later subsurface use
        self.icons = pygame.image.load(Config.assets_path("icons.png"))
        # Initialize all the GUI elements for MENU state
        self._initialize_menu_elements()
        # Initialize all the GUI elements for PLAY state
        self._initialize_play_elements()
        # Container for tracking all the floaters that will be spawned
        self._floaters = []

    def _initialize_menu_elements(self):
        """
        Creates the GUI for the MENU state of the game.
        """
        wtitle, htitle = self._WIDTH-300, 100
        bwidth, bheight = 180, 65
        xtitle, ytitle = (self._WIDTH-wtitle) / 2, (self._HEIGHT-htitle) / 2-80
        xbtn, ybtn = (self._WIDTH-bwidth) / 2, ytitle + htitle + 40

        # Create a black transparent menu panel
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-5, -5, self._WIDTH+10, self._HEIGHT+10),
            starting_height=10, manager=self.manager, object_id="#menu_panel"
        )
        # Create the Game Title
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(xtitle, ytitle, wtitle, htitle),
            text="SNAKE GAME", container=self.menu_panel,
            object_id="#game_title_lbl"
        )
        # Create the Start Button of the Menu
        self._start_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(xbtn, ybtn, bwidth, bheight),
            text="START", container=self.menu_panel,
            object_id="#start_btn"
        )

    def _initialize_play_elements(self):
        """
        Creates the GUI for the PLAY state of the game.
        """
        score_width = 200
        lifetime_width = 200
        stretch_width = 185

        # Create game panel strip at the top of the screen
        self.game_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, -5, self._WIDTH, 50),
            starting_height=5, manager=self.manager, object_id="#game_panel"
        )
        self.game_panel.hide()
        # Create the score label
        score_pos_x = self.game_panel.rect.center[0] - (score_width / 2) - 10
        self._score_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(score_pos_x, 0, score_width, 35),
            text="SCORE: 0", container=self.game_panel, object_id="#score_lbl"
        )
        # Create the lifetime label
        self._lifetime_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(45, 0, lifetime_width, 35),
            text="LIFETIME: 100", container=self.game_panel,
            object_id="#lifetime_lbl"
        )
        # Create the life icon
        self.heart_icon = self.icons.subsurface((0, 0, 65, 60))
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(10, 2, 30, 30),
            image_surface=self.heart_icon,
            container=self.game_panel
        )
        # Create the stretch label (length of the snake)
        stretch_pos_x = self.game_panel.rect.width - stretch_width
        self._stretch_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(stretch_pos_x, 0, stretch_width, 35),
            text="STRETCH: 0m", container=self.game_panel,
            object_id="#stretch_lbl"
        )
        # Create the stretch icon
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(stretch_pos_x - 35, 2, 30, 30),
            image_surface=self.icons.subsurface((65, 0, 55, 55)),
            container=self.game_panel
        )

    def update(self):
        """ Updates manually some of the animations for GUI elements. """
        match self.state:
            case GAMESTATE.PLAY:
                for floater in self._floaters:
                    floater.update()

    def draw(self):
        """ Draws some GUI elements that are not included in the Manager. """
        match self.state:
            case GAMESTATE.PLAY:
                for floater in self._floaters:
                    floater.draw(self.screen)

    def process_events(self, event):
        """ Checks for events related to pygame_gui elements."""
        # TEXT EFFECT FINISHED EVENT
        if event.type == pygame_gui.UI_TEXT_EFFECT_FINISHED:
            if event.ui_element.get_object_id() == "@regen_lbl":
                # Find the label element in the floater to destroy
                for floater in self._floaters:
                    if event.ui_element == floater.label:
                        floater.destroy()
                        self._floaters.remove(floater)
                        break

    def spawn_regen_label(self, position, regen):
        """ Spawns a label that shows the regen stat after eating food. """
        floater = Floater(name="regen", position=position,
                          dimension=(45, 40), text=f"+{regen}",
                          icon=self.heart_icon, isize=30)
        self._floaters.append(floater)

    def update_score(self, score):
        """ Updates the score label with current score of the game. """
        self._score_lbl.set_text(f"SCORE: {score}")

    def update_lifetime(self, lifetime):
        """ Updates the lifetime label with current lifetime of the game. """
        self._lifetime_lbl.set_text(f"LIFETIME: {lifetime:.1f}")

    def update_stretch(self, stretch):
        """ Updates the stretch label with current length of the snake. """
        self._stretch_lbl.set_text(f"STRETCH: {stretch}m")
