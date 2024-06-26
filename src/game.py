"""
Game Class - game.py
-----------------------------------------------------------
This class is responsible for handling the game logic,
keyboard and window events, and rendering the game objects.
This handles the main logic decisions of the game and
calls object methods accordingly.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
import pygame_gui
import random
import marshal
from interface import Interface
from src.config import Config
from src.config import GAMESTATE
from src.objects.snake import Snake
from src.objects.food import Food
from src.objects.foodbuff import FoodBuff
from src.objects.speedup import SpeedUp
from src.objects.slowdown import SlowDown
from src.objects.bomb import Bomb


class Game:

    def __init__(self, screen: pygame.Surface, manager: pygame_gui.UIManager):
        """
        Initialization of game objects and parameters.
        """
        self.HEIGHT = Config.SCREEN_HEIGHT
        self.WIDTH = Config.SCREEN_WIDTH
        self.screen = screen
        self.manager = manager
        self.state = GAMESTATE.MENU
        self.bounderies = pygame.Rect(10, 10, self.WIDTH - 20, self.HEIGHT - 20)

        # Initialize the game interface manager
        self.interface = Interface(screen, manager)
        # Load the game background and the panel image
        self._load_game_backgrounds()
        # These variables are used for various flags regarding the snake
        self._auto_path_counter = 0
        self._gameover_counter = 0.15
        self._interface_gameover_delay = 0.2
        self._uturn = None
        # Create the Snake object as the player and pass the game background
        self.snake = Snake(background=self.bgwalled)
        # Create a starting Food Object (creation at play button press)
        self.apple = None
        self.golden_apple = None
        # Create the starting item buffs (creation at play button press)
        self.speedup = None
        # Create the debuff items (creation at play button press)
        self.slowdown = None
        # Create and initialize the bombs based on config count
        self.bombs = []
        for _ in range(Config.BOMB_COUNT):
            self.bombs.append(Bomb(damage=10, deduction=50, snake=self.snake))
        # Score and total time of the current game
        self.score = 0
        self.total_time = 0
        # Create the empty list of leaderboard entries
        self.lb_data = []
        # Load the leaderboard data if it's available in data folder
        lb_path = Config.BASE_PATH / "data/leaderboard.bin"
        if lb_path.exists():
            self.lb_data = marshal.loads(lb_path.read_bytes())
        # Initialize the leaderboard GUI
        self.interface.update_leaderboard_data(self.lb_data[:3])

    def _load_game_backgrounds(self):
        """ Loads the background image and the walls on each window. """
        raw_bg = pygame.image.load(Config.assets_path("background.png"))
        self.bg = pygame.transform.scale(raw_bg, (self.WIDTH, self.HEIGHT))
        panel = pygame.image.load(Config.assets_path("panel.png"))
        # Get only a part of the panel background to make as a wall
        self.wall_top = panel.subsurface(0, 25, 994, 25)
        self.wall_bottom = pygame.transform.rotate(self.wall_top, 180)
        self.wall_left = pygame.transform.rotate(self.wall_top, 90)
        self.wall_right = pygame.transform.rotate(self.wall_top, -90)
        # Create a walled background for the snake
        self.bgwalled = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.bgwalled.blit(self.bg, (0, 0))
        self.bgwalled.blit(self.wall_left, (0, 0))
        self.bgwalled.blit(self.wall_right, (self.WIDTH - 25, 0))
        self.bgwalled.blit(self.wall_top, (15, 0))
        self.bgwalled.blit(self.wall_bottom, (15, self.HEIGHT - 22))

    def reset_game(self):
        """
        This will be called in events to reset the game state to new game.
        All variables that needs to return to initial value should be put here.
        """
        self.snake = Snake(background=self.bgwalled)
        self._gameover_counter = 0.15
        self._interface_gameover_delay = 0.2
        self._auto_path_counter = 0
        self._uturn = False
        self.score = 0
        self.total_time = 0
        # Destroy and reset all bombs
        for bomb in self.bombs:
            bomb.reset()

    def update(self, time_delta):
        """
        Handles the game logic. Updates the game objects and status.
        This also is passed the time_delta computation from the main loop.
        """
        # HANDLE MENU UPDATES
        if self.state == GAMESTATE.MENU:
            # Update the snake for the menu auto path
            self.snake_menu_auto_path_update(time_delta)

        # HANDLE PLAY UPDATES
        elif self.state == GAMESTATE.PLAY:
            # Reduce the life of the player based on the passed time
            self.snake.lifetime -= time_delta
            self.total_time += time_delta
            self.interface.update_lifetime(max(0, self.snake.lifetime))

            # Update the snake if it collides with the food and eats it
            self.snake_eat_food_update(self.apple)
            self.snake_eat_food_update(self.golden_apple)

            # Update the snake if it collides with the items and eats it
            self.snake_eat_items_update(self.speedup)
            self.snake_eat_items_update(self.slowdown)

            # Update the snake if it collides with the bombs
            self.snake_collide_bombs_update()

            # Update the food objects for its animation states
            self.apple.update(time_delta)
            self.golden_apple.update(time_delta)

            # Check if the snake head collides with its body parts
            self.snake_collide_self_checker(time_delta)
            # Check if the snake collides with the window bounderies
            self.snake_bump_bounderies_update()

            # Update the buff items for animation states
            self.speedup.update(time_delta)
            # Update the debuff items for animation states
            self.slowdown.update(time_delta)

            # Update the instantiated bombs on PLAY States
            for bomb in self.bombs:
                bomb.update(time_delta)

            # Reduce the gameover counter if the lifetime of snake reaches 0
            if self.snake.lifetime <= 0:
                self._gameover_counter -= time_delta

            # Call the gameover event if the counter reaches 0
            if self._gameover_counter <= 0:
                self.set_gameover_event()

        # HANDLE GAMEOVER EVENTS
        elif self.state == GAMESTATE.GAMEOVER:
            if self._interface_gameover_delay > 0:
                counter = max(0, self._interface_gameover_delay - time_delta)
                self._interface_gameover_delay = counter
            elif self._interface_gameover_delay == 0:
                self.show_gameover_screen()

        # UPDATE MOVEMENT OF SNAKE IN MENU AND PLAY STATES
        if self.state == GAMESTATE.MENU or self.state == GAMESTATE.PLAY:
            # Update the movement of the snake
            self.snake.update(time_delta)

        # Update the Interface Manager for animation of some elements
        self.interface.update()

    def game_events(self):
        """
        Handles the pygame events (QUIT and keyboard events).
        Returns False for it to signal the game loop to stop.
        Custom events of some game objects are also handled here.
        """
        # HELPER FUNCTIONS FOR THE GAME EVENTS
        def instantiate_foods():
            self.apple = Food(filename="apple.png", points=10, regen=2)
            self.golden_apple = FoodBuff(filename="goldapple.png",
                                         points=50, regen=5)

        def instantiate_items():
            self.speedup = SpeedUp(name="speedup", filename="speedup.png",
                                   points=20, value=5, negative=False)
            self.slowdown = SlowDown(name="slowdown", filename="snail.png",
                                     points=10, value=2, negative=True)

        def all_territories():
            return ([self.apple.territory, self.golden_apple.territory,
                    self.speedup.territory, self.slowdown.territory] +
                    self.snake.rects)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # GUI Manager pass each event to the pygame_gui
            self.manager.process_events(event)
            # Pass the event also to the interface manager
            self.interface.process_events(event)

            # PLAY KEYBOARD EVENTS
            if self.state == GAMESTATE.PLAY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.snake.move(Snake.LEFT)
                    if event.key == pygame.K_d:
                        self.snake.move(Snake.RIGHT)
                    if event.key == pygame.K_w:
                        self.snake.move(Snake.UP)
                    if event.key == pygame.K_s:
                        self.snake.move(Snake.DOWN)

            # GUI BUTTON EVENTS
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # START BUTTON EVENT
                if event.ui_element == self.interface.start_btn:
                    self.state = GAMESTATE.PLAY
                    self.interface.start_game_event()
                    # Instatiate the apple food and golden apple
                    instantiate_foods()
                    # Instantiate also the buff items
                    instantiate_items()

                # RESTART BUTTON EVENT
                elif event.ui_element == self.interface.restart_btn:
                    # Perform saving of leaderboard data
                    self.update_leaderboard_data()
                    # Prepare for restart of gameplay
                    self.state = GAMESTATE.PLAY
                    self.interface.restart_game_event()
                    self.reset_game()
                    # Reset the food objects
                    instantiate_foods()
                    # Reset the buff items
                    instantiate_items()

                # QUIT BUTTON EVENT
                elif event.ui_element == self.interface.quit_btn:
                    # Perform saving of leaderboard data
                    self.update_leaderboard_data()
                    # Prepare for quitting of gameplay
                    self.state = GAMESTATE.MENU
                    self.interface.main_menu_event()
                    self.reset_game()

            # SPAWN FOOD EVENT
            if self.state == GAMESTATE.PLAY:
                if event.type == Food.SPAWN_FOOD_EVENT:
                    self.apple.spawn(off_limits_rects=all_territories())
                if event.type == FoodBuff.SPAWN_FOOD_BUFF_EVENT:
                    self.golden_apple.spawn(off_limits_rects=all_territories())

            # SPAWN ITEMS EVENT
            if self.state == GAMESTATE.PLAY:
                if event.type == SpeedUp.SPAWN_SPEED_UP_EVENT:
                    self.speedup.spawn(off_limits_rects=all_territories())
                if event.type == SlowDown.SPAWN_SLOW_DOWN_EVENT:
                    territory = all_territories()
                    self.slowdown.spawn_near_head(head=self.snake.head,
                                                  off_limits_rects=territory)

        return True

    def draw(self):
        """
        Draws the game objects on the screen.
        """
        # Draw the background first
        self.screen.blit(self.bg, (0, 0))
        # Draw the walls on every boundery of the screen
        self.screen.blit(self.wall_left, (0, 0))
        self.screen.blit(self.wall_right, (self.WIDTH - 25, 0))
        self.screen.blit(self.wall_top, (15, 0))
        self.screen.blit(self.wall_bottom, (15, self.HEIGHT - 22))

        # Draw the snake which is available in any MODE
        self.snake.draw(self.screen)

        # Draw game objects that are only viewable in PLAY mode
        if self.state == GAMESTATE.PLAY or self.state == GAMESTATE.GAMEOVER:
            # Draw the available bombs
            for bomb in self.bombs:
                bomb.draw(self.screen)
            # Draw the powerups and items
            self.apple.draw(self.screen)
            self.golden_apple.draw(self.screen)
            self.speedup.draw(self.screen)
            self.slowdown.draw(self.screen)

        # Draw the GUI elements from Inteface
        self.interface.draw()

    def snake_menu_auto_path_update(self, time_delta):
        """
        This will randomize the movement of the snake in the menu.
        It must not go over the bounderies of the window
        Every second it will randomize a direction of the head.
        """
        xhead, yhead = self.snake.head.bounds.topleft
        direction = self.snake.head.direction
        topmax, botmax = 80, self.HEIGHT - 120
        leftmax, rightmax = 80, self.WIDTH - 120

        if not self._uturn and (yhead < topmax or yhead > botmax):
            self.snake.move(random.choice([Snake.LEFT, Snake.RIGHT]))
            self._auto_path_counter = 0.3
            self._uturn = [Snake.DOWN] if yhead < topmax else [Snake.UP]

        if not self._uturn and (xhead < leftmax or xhead > rightmax):
            self.snake.move(random.choice([Snake.UP, Snake.DOWN]))
            self._auto_path_counter = 0.3
            self._uturn = [Snake.RIGHT] if xhead < leftmax else [Snake.LEFT]

        if self._auto_path_counter >= 0.7:
            # Remove the current direction and its opposite direction
            moves = [Snake.UP, Snake.DOWN, Snake.LEFT, Snake.RIGHT]
            if self._uturn:
                moves = self._uturn
            else:
                to_remove = [direction, direction * -1]
                moves = [move for move in moves if move not in to_remove]

            # Randomize the next valid moves
            next_move = random.choice(moves)
            self.snake.move(next_move)
            self._auto_path_counter = -0.3 if self._uturn else 0
            self._uturn = None

        self._auto_path_counter += time_delta

    def snake_eat_food_update(self, food):
        """
        Checks if the snake head collides with the specified food.
        If it collides then destroy the food and grow the snake.
        """
        if food.spawned:
            if self.snake.head.bounds.colliderect(food.bounds):
                # Spawn a regen label
                apple_pos = pygame.Vector2(food.bounds.topleft)
                self.interface.spawn_regen_label(apple_pos, food.regen,
                                                 food.points)
                # Update the score add the health regen
                self.score += food.points
                self.snake.lifetime += food.regen
                # Update the game labels
                self.interface.update_score(self.score)
                self.interface.update_stretch(self.snake.stretch)
                # Destroy the apple and grow the snake
                self.snake.grow()
                food.destroy()

    def snake_eat_items_update(self, item):
        """
        Checks if the snake head collides with the specified item.
        If it collides determine the type of item and apply the
        buff into the snake object.
        """
        if item.spawned:
            if self.snake.head.bounds.colliderect(item.bounds):
                # Display a buff icon and points floater
                item_pos = pygame.Vector2(item.bounds.topleft)
                self.interface.spawn_buff_label(buff_icon=item.image.copy(),
                                                position=item_pos,
                                                buff_value=item.value,
                                                points=item.points,
                                                negate=item.negative)
                # Apply the buff item to the snake head
                self.snake.apply_buff(item)
                # Add the score and update the game labels
                self.score += item.points
                self.interface.update_score(self.score)
                # Destroy the item
                item.destroy()

    def snake_collide_bombs_update(self):
        """
        Checks for the collision of bombs into the head of the snake.
        If it collides then reduce the health and score of the player,
        also trigger the explosion of the bomb and show the negative red
        floater object for the bomb.
        """
        for bomb in self.bombs:
            if bomb.spawned and self.snake.head.bounds.colliderect(bomb.bounds):
                # Display a buff icon and points floater
                item_pos = pygame.Vector2(bomb.bounds.topleft)
                self.interface.spawn_bomb_label(position=item_pos,
                                                damage=bomb.damage,
                                                deduction=bomb.deduction)
                # Reduce the score and health then update the labels
                self.snake.trigger_damaged()
                self.score = max(0, self.score - bomb.deduction)
                self.snake.lifetime = max(0, self.snake.lifetime - bomb.damage)
                self.interface.update_score(self.score)
                # If lifetime reaches 0 then reconfig the gameover counter
                if self.snake.lifetime <= 0:
                    self._gameover_counter = 0.35
                # Destroy the bomb to respawn it again
                bomb.destroy()
                break

    def snake_bump_bounderies_update(self):
        """
        Check if each head part collides with window bounderies
        If it collides then the snake is dead, and it's game over.
        Set the game over counter to 0, the code to trigger the whole
        game over event is found in the snake_collide_self_checker.
        """
        snake_head = self.snake.head
        if snake_head.bounds.clamp(self.bounderies) != snake_head.bounds:
            self._gameover_counter = 0
            # Instant hide the game panel if the collision is on top bounds
            if self.snake.head.rect.y < 70:
                self.interface.game_panel.hide()

    def snake_collide_self_checker(self, time_delta):
        """
        Checks if the head part collides with any of the moving snake parts.
        If the condition is true, reduce the gameover counter delay in order
        for the snake to collide with its body.
        """
        for body in self.snake.body[1:]:
            if self.snake.head.bounds.colliderect(body.bounds):
                counter = max(0, self._gameover_counter - time_delta)
                self._gameover_counter = counter
                break

    def set_gameover_event(self):
        """
        If the gameover counter reaches zero, then set state to GAMEOVER
        We also need to compute the death moment location of the snake
        And finally pass the final game data to the results panel
        """
        # Set the game state to GAMEOVER
        self.state = GAMESTATE.GAMEOVER
        self._gameover_counter = -1

        # Remove the floaters
        self.interface.destroy_floaters()

        # Set the dead image sprite of the snake head
        self.snake.die()
        self.snake.draw(self.screen)

        # Pass the final game data to the results panel
        self.interface.update_results_data(score=self.score,
                                           stretch=self.snake.stretch,
                                           lifetime=self.total_time)

    def show_gameover_screen(self):
        """
        This will be called after the delay is finished when setting
        the GAMEOVER flag. This allows the game to update and remove
        remaining game UI and effects
        """
        # Set the moments image of the snake in the gameover screen
        width, height, (x, y) = 320, 180, self.snake.head.bounds.topleft
        snakepos = (x - (width // 3) - 20, y - (height // 3))
        moments_rect = pygame.Rect(*snakepos, width, height)
        moments_rect = moments_rect.clamp(self.screen.get_rect())
        moments = self.screen.subsurface(moments_rect)
        life_left = int(self.snake.lifetime)
        self.interface.update_moments_image(moments, life_left)

        # Finally set the interface to gameover
        self._interface_gameover_delay = -1
        self.interface.gameover_event()

    def update_leaderboard_data(self):
        """
        This method will add a new leaderboard data and sort it by descending
        order of scores to show the top 3 in the leaderboard UI.
        The data that it will get will be the current status of the game.
        """
        # Get the current game stats
        data = {"name": self.interface.get_player_name(),
                "score": self.score, "stretch": self.snake.stretch,
                "lifetime": int(self.total_time)}
        # Append it to current lb_data variable
        self.lb_data.append(data)
        # Sort it by score
        self.lb_data.sort(key=lambda x: x["score"], reverse=True)
        # Pass the top 3 to the interface leaderboard UI generator
        self.interface.update_leaderboard_data(self.lb_data[:3])
        # Parse the leaderboard data to json and save it in file
        byte_data = marshal.dumps(self.lb_data)
        save_path = Config.BASE_PATH / "data/leaderboard.bin"
        save_path.write_bytes(byte_data)
