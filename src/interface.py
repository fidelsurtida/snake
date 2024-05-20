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
        # Initialize all the GUI elements for GAMEOVER state
        self._initialize_gameover_elements()
        # Container for tracking all the floaters that will be spawned
        self._floaters = []
        # Create a name flag for saving the player name
        self._saved_name = None

    def _initialize_menu_elements(self):
        """
        Creates the GUI for the MENU state of the game.
        """
        wtitle, htitle = self._WIDTH - 300, 100
        lb_width, lb_height, item_width = wtitle - 20, 165, wtitle - 40
        bwidth, bheight = 230, 70
        margin_y, hlbitem = 13, 40
        xtitle, ytitle = ((self._WIDTH - wtitle) / 2,
                          (self._HEIGHT - htitle) / 2 - 150)

        # Create a black transparent menu panel
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-5, -5, self._WIDTH+10, self._HEIGHT+10),
            starting_height=10, manager=self.manager, object_id="#menu_panel"
        )
        # Create the Game Title
        title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(xtitle, ytitle, wtitle, htitle),
            text="SNAKE GAME", container=self.menu_panel,
            object_id="#game_title_lbl"
        )
        # Create the leaderboard panel
        top_left = (title.rect.bottomleft + pygame.Vector2(10, margin_y))
        self.leaderboard_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(*top_left, lb_width, lb_height),
            starting_height=1, manager=self.manager,
            container=self.menu_panel, object_id="#leaderboard_panel"
        )
        # Create the leaderboard title label
        top_left = top_left + pygame.Vector2(2, 0)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(*top_left, lb_width - 4, hlbitem),
            text="LEADERBOARD TOP 3", container=self.menu_panel,
            object_id="#leaderboard_lbl"
        )

        # Create the leaderboard items. Call the helper method
        self._initialize_leaderboard_items(item_width, hlbitem)

        # Create the Start Button of the Menu
        lb_y = self.leaderboard_panel.rect.bottom
        top_left = ((self._WIDTH-bwidth) / 2, lb_y + margin_y)
        self.start_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(*top_left, bwidth, bheight),
            text="    START", container=self.menu_panel,
            object_id="#start_btn"
        )
        # Create the start icon from the icons image
        top_left = self.start_btn.rect.topleft + pygame.Vector2(23, 10)
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(*top_left, 51, 51),
            image_surface=self.icons.subsurface((2, 61, 51, 51)),
            container=self.menu_panel
        )
        # Create the developed by label
        label_rect = pygame.Rect((self._WIDTH-410)/2, self._HEIGHT-60, 410, 20)
        pygame_gui.elements.UILabel(
            relative_rect=label_rect, object_id="#developed_lbl",
            text="Developed by:  2024 © Fidel Jesus O. Surtida I",
            container=self.menu_panel
        )

    def _initialize_leaderboard_items(self, item_width, hlbitem):
        """
        This will be called to recreate the leaderboard elements based
        on the saved highscore data file.
        """
        # Create the panel list to save the references
        self.entry_panels = []
        # Create the medal icons
        medals = [
            self.icons.subsurface(1, 117, 27, 27),
            self.icons.subsurface(35, 119, 27, 28),
            self.icons.subsurface(63, 118, 27, 27)
        ]
        # UI measurement variables
        name_width, stats_width, rank_width = 150, 80, 50
        entry_y, lbl_height = hlbitem - 3, 35
        # Sample data to be displayed in the top 3
        data = {
            1: {"name": "DivineKaiser", "score": 12345,
                "lifetime": 7777, "stretch": 123},
            2: {"name": "HeraLithea", "score": 12345,
                "lifetime": 3333, "stretch": 456},
            3: None
        }

        # Loop throught the data and create each an entry item UI
        for rank, player in data.items():
            # Create the leaderboard entry panel container
            entry_panel = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect(3, entry_y, item_width, hlbitem),
                starting_height=1, manager=self.manager,
                container=self.leaderboard_panel, object_id="@entry_panel"
            )
            # Create the medal image
            pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(15, 5, 25, 25),
                image_surface=medals[rank-1], container=entry_panel
            )
            # Create the position label
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(35, 0, rank_width, lbl_height),
                text=f"{rank}", container=entry_panel,
                object_id="@rank_labels"
            )
            # Create the player name label
            player_name = player["name"] if player else "-----"
            name_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(95, 0, name_width, lbl_height),
                text=player_name, container=entry_panel,
                object_id="@entry_labels"
            )
            # Create the score icon image
            x = name_label.relative_rect.right + 30
            score_img = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(x, 5, 25, 23),
                image_surface=self.icons.subsurface((157, 1, 30, 28)),
                container=entry_panel
            )
            # Create the score label
            x = score_img.relative_rect.right + 10
            player_score = player["score"] if player else "-----"
            score_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(x, 0, stats_width, lbl_height),
                text=f"{player_score}", container=entry_panel,
                object_id="@entry_num_labels"
            )
            # Create the lifetime icon image
            x = score_label.relative_rect.right + 20
            lifetime_img = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(x, 3, 23, 27),
                image_surface=self.icons.subsurface((159, 31, 26, 31)),
                container=entry_panel
            )
            # Create the lifetime label
            x = lifetime_img.relative_rect.right + 10
            player_lifetime = f"{player["lifetime"]}s" if player else "-----"
            lifetime_label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(x, 0, stats_width, lbl_height),
                text=player_lifetime, container=entry_panel,
                object_id="@entry_num_labels"
            )
            # Create the stretch icon image
            x = lifetime_label.relative_rect.right + 20
            stretch_img = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(x, 3, 23, 27),
                image_surface=self.icons.subsurface((65, 0, 55, 55)),
                container=entry_panel
            )
            # Create the stretch label
            x = stretch_img.relative_rect.right + 10
            player_stretch = f"{player["stretch"]}m" if player else "-----"
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(x, 0, stats_width, lbl_height),
                text=player_stretch, container=entry_panel,
                object_id="@entry_num_labels"
            )
            # append the entry panel and update the y coordinate
            self.entry_panels.append(entry_panel)
            entry_y += hlbitem - 5

    def _initialize_gameover_elements(self):
        """
        Creates the GUI for the GAMEOVER state of the game.
        """
        wtitle, htitle = self._WIDTH - 370, 120
        bwidth, bheight = 230, 70
        picwidth, picheight = 340, 200
        res_width, res_height = wtitle - 50, 80
        res_col = res_width / 3
        xtitle = (self._WIDTH - wtitle) / 2
        ytitle = (self._HEIGHT - htitle) / 4

        # Create a black transparent gameover panel
        self.gameover_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(-5, -5, self._WIDTH+10, self._HEIGHT+10),
            starting_height=10, manager=self.manager,
            object_id="#gameover_panel"
        )
        self.gameover_panel.hide()
        # Create the game over title label
        gameover_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(xtitle, ytitle, wtitle, htitle),
            text="GAME OVER", container=self.gameover_panel,
            object_id="#gameover_lbl"
        )
        # Create a results panel
        top_left = (gameover_lbl.rect.bottomleft +
                    pygame.Vector2(25, 15))
        self.results_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(*top_left, res_width, res_height),
            starting_height=10, manager=self.manager,
            object_id="#results_panel", container=self.gameover_panel
        )
        # Create the player label
        player_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, res_col, 38),
            container=self.results_panel, object_id="#player_lbl",
            text="     PLAYER NAME"
        )
        # Create the player icon beside the label
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(15, 3, 30, 31),
            image_surface=self.icons.subsurface((125, 25, 30, 32)),
            container=self.results_panel
        )
        # Create the player name textbox for the player to enter his/her name
        top_left = player_lbl.relative_rect.bottomleft
        self._results_player_name = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(*top_left, res_col, 30),
            container=self.results_panel, object_id="#results_player_textbox",
            placeholder_text="Enter Name Here..."
        )
        # Create the stretch icon beside the label
        stretch_icon = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(res_col + 15, 3, 27, 27),
            image_surface=self.icons.subsurface((65, 0, 55, 55)),
            container=self.results_panel
        )
        # Create the stretch label
        self._results_stretch_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(res_col + 50, 0, res_col - 40, 35),
            container=self.results_panel, object_id="#results_stretch_lbl",
            text="STRETCH: 0m"
        )
        # Create the lifetime icon beside the label
        top_left = stretch_icon.relative_rect.bottomleft + pygame.Vector2(0, 2)
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(*top_left, 26, 31),
            image_surface=self.icons.subsurface((159, 31, 26, 31)),
            container=self.results_panel
        )
        # Create the lifetime label
        top_left = self._results_stretch_lbl.relative_rect.bottomleft
        self._results_lifetime_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(*top_left, res_col - 30, 30),
            container=self.results_panel, object_id="#results_lifetime_lbl",
            text="LIFETIME: 0s"
        )
        # Create the total score label
        total_score = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(res_col * 2, 0, res_col, 38),
            container=self.results_panel, object_id="#total_score_lbl",
            text="     TOTAL SCORE"
        )
        # Create the total score icon beside the label
        self.score_icon = self.icons.subsurface((157, 1, 30, 28))
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(res_col * 2 + 15, 6, 30, 28),
            image_surface=self.score_icon, container=self.results_panel
        )
        # Create the results total score label (real score goes here)
        top_left = total_score.relative_rect.bottomleft
        self._results_score_lbl = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(*top_left, res_col, 30),
            container=self.results_panel, object_id="#results_score_lbl",
            text="0"
        )
        # Create the restart button
        top_left = (self.results_panel.rect.bottomright +
                    pygame.Vector2(-bwidth, 35))
        self.restart_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(*top_left, bwidth, bheight),
            text="    RETRY", container=self.gameover_panel,
            object_id="#restart_btn"
        )
        # Create the restart icon from the icons image
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(*top_left + (25, 8), 50, 50),
            image_surface=self.icons.subsurface((55, 61, 50, 50)),
            container=self.gameover_panel
        )
        # Create the quit button
        top_left = self.restart_btn.rect.bottomleft + pygame.Vector2(0, 30)
        self.quit_btn = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(*top_left, bwidth, bheight),
            text="  QUIT", container=self.gameover_panel,
            object_id="#quit_btn"
        )
        # Create the quit icon from the icons image
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(*top_left + (28, 8), 50, 50),
            image_surface=self.icons.subsurface((107, 61, 50, 50)),
            container=self.gameover_panel
        )
        # Create the last moments panel
        top_left = self.results_panel.rect.bottomleft + pygame.Vector2(0, 18)
        moments_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(*top_left, picwidth, picheight),
            starting_height=10, manager=self.manager,
            object_id="#last_moments_panel", container=self.gameover_panel
        )
        # Create the image holder for the last moments
        self.moments_image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(0, 0, picwidth - 20, picheight - 20),
            image_surface=pygame.Surface((picwidth, picheight)),
            container=moments_panel
        )
        # Create the deathcam label
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, 120, 25),
            text="DEATHCAM  ", container=moments_panel,
            object_id="#deathcam_lbl"
        )
        # Create the deathcam icon from the icons image
        pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(5, 3, 20, 18),
            image_surface=self.icons.subsurface((131, 4, 20, 18)),
            container=moments_panel
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
            relative_rect=pygame.Rect(0, -55, self._WIDTH, 50),
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
                # Animate the gamepanel to go down when the game starts
                if self.game_panel.rect.y < -5:
                    pos = pygame.Vector2(self.game_panel.rect.topleft)
                    self.game_panel.set_position(pos + pygame.Vector2(0, 1))

            case GAMESTATE.GAMEOVER:
                # Animate the gamepanel to go up when the game ends
                if self.game_panel.rect.y > -55:
                    pos = pygame.Vector2(self.game_panel.rect.topleft)
                    self.game_panel.set_position(pos - pygame.Vector2(0, 1))

        # Update the floaters if it exists regardless of the state
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

    def main_menu_event(self):
        """ Sets the gamestate and shows the menu panel. """
        self.state = GAMESTATE.MENU
        self.menu_panel.show()
        self.game_panel.hide()
        self.gameover_panel.hide()
        self.update_score(0)
        self.update_lifetime(100)
        self.update_stretch(0)
        # Reset the saved player names
        self._saved_name = None
        self._results_player_name.set_text("")

    def start_game_event(self):
        """ Sets the gamestate and hides the menu panel. """
        self.state = GAMESTATE.PLAY
        self.menu_panel.hide()
        self.game_panel.show()

    def restart_game_event(self):
        """ Restarts a new game and resets the game panel labels. """
        self.state = GAMESTATE.PLAY
        self.game_panel.show()
        self.gameover_panel.hide()
        self.update_score(0)
        self.update_lifetime(100)
        self.update_stretch(0)
        # Save the player name
        self._saved_name = self._results_player_name.get_text() or "PLAYER"

    def gameover_event(self):
        """ Sets the gamestate and shows the gameover panel. """
        self.state = GAMESTATE.GAMEOVER
        self.gameover_panel.show()
        # If there is a saved player name then replace it to the textbox
        if self._saved_name:
            self._results_player_name.set_text(self._saved_name)

    def spawn_regen_label(self, position, regen, points):
        """ Spawns a label that shows the regen stat after eating food. """
        floater = Floater(name="regen", position=position - (35, 0),
                          dimension=(35, 30), text=f"+{regen}",
                          icon=self.heart_icon, isize=25)
        point_floater = Floater(name="points", position=position + (30, 0),
                                dimension=(40, 30), text=f"{points}",
                                icon=self.score_icon, isize=25)
        self._floaters.append(floater)
        self._floaters.append(point_floater)

    def spawn_buff_label(self, buff_icon, position, buff_value, points, negate):
        """ Spawns a floating label that shows buff acquired and points. """
        buff_icon.set_alpha(255)
        vlabel = "-" if negate else "+"
        buff_float = Floater(name="buff", position=position - (35, 0),
                             dimension=(35, 30), text=f"{vlabel}{buff_value}",
                             icon=buff_icon, isize=30)
        point_floater = Floater(name="points", position=position + (30, 0),
                                dimension=(40, 30), text=f"{points}",
                                icon=self.score_icon, isize=25)
        self._floaters.append(buff_float)
        self._floaters.append(point_floater)

    def update_score(self, score):
        """ Updates the score label with current score of the game. """
        self._score_lbl.set_text(f"SCORE: {score}")

    def update_lifetime(self, lifetime):
        """ Updates the lifetime label with current lifetime of the game. """
        self._lifetime_lbl.set_text(f"LIFETIME: {lifetime:.1f}")

    def update_stretch(self, stretch):
        """ Updates the stretch label with current length of the snake. """
        self._stretch_lbl.set_text(f"STRETCH: {stretch}m")

    def update_results_data(self, *, score="0",
                            stretch="0", lifetime="0"):
        """ Updates the results panel with the final game data. """
        self._results_stretch_lbl.set_text(f"STRETCH:  {stretch}m")
        self._results_lifetime_lbl.set_text(f"LIFETIME:  {lifetime:.0f}s")
        self._results_score_lbl.set_text(f"{score}")

    def get_player_name(self):
        """ Gets the player name in the gameover player textbox. """
        return self._results_player_name.get_text()

    def update_moments_image(self, image):
        """ Updates the last moments image with the given image. """
        self.moments_image.set_image(image)
        self.moments_image.rebuild()
