"""
Bomb Class - bomb.py
-----------------------------------------------------
This module contains the Bomb Class that when spawned
it has a timer for how long before exploding and a
delay timer for it to spawn again. When the player
or snake hits this bomb, it will reduce its health
and deduct some score points.
-----------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------
"""
import pygame
import random
from pygame.sprite import Sprite
from src.config import Config


class Bomb(Sprite):

    # Bomb Settings from Config
    SIZE = Config.BOMB_SIZE
    LIFETIME = Config.BOMB_LIFETIME
    SPAWN_DELAY_MIN = Config.BOMB_MIN_SPAWN_DELAY
    SPAWN_DELAY_MAX = Config.BOMB_MAX_SPAWN_DELAY
    SCALE_TIME = 0.5

    def __init__(self, *, damage, deduction):
        """
        Initializes the bomb image as sprite and starts the countdown of
        the delay timer to spawn the bomb. Initialize also the counters
        for lifetime and scale timers.
        """
        super().__init__()
        self._img = pygame.image.load(Config.assets_path("bomb.png"))
        self.image = pygame.transform.scale(self._img, (0, 0))
        self.spawned = False
        self.damage = damage
        self.deduction = deduction
        self._spawn_delay = self._generate_spawn_delay()
        self._lifetime = self.LIFETIME
        self._swidth = Config.SCREEN_WIDTH
        self._sheight = Config.SCREEN_HEIGHT

    def _generate_spawn_delay(self):
        """ Generates a random number for the spawn delay attribute. """
        return random.randint(self.SPAWN_DELAY_MIN, self.SPAWN_DELAY_MAX)

    def _spawn_bomb(self):
        """
        Spawns the bomb object in a random position based on screen
        dimensions and the passed off limits object territories.
        """
        x = random.randint(self.SIZE, self._swidth - self.SIZE * 2)
        y = random.randint(self.SIZE + 50, self._sheight - self.SIZE * 2)
        rect = pygame.Rect(x + self.SIZE // 2, y + self.SIZE // 2, 0, 0)
        # Initialize the final valid position of this bomb object
        # Save the start position and end position in reference for scaling
        self._sposition = pygame.Vector2(rect.x, rect.y)
        self._eposition = pygame.Vector2(x, y)
        self._lifetime = self.LIFETIME
        self.rect = rect
        self.spawned = True

    def update(self, time_delta):
        """ Updates the attributes of the bomb object. """
        # If not spawned then reduce the delay timer
        if not self.spawned:
            self._spawn_delay = max(0, self._spawn_delay - time_delta)
            # Call the spawn method if the spawn delay reaches 0
            if self._spawn_delay == 0:
                self._spawn_bomb()

        # Else if spawned then reduce the lifetime
        if self.spawned:
            self._lifetime = max(0, self._lifetime - time_delta)

            # If lifetime is full until the decrease of SCALE TIME
            # Animate to scale up and also adjust the rect accordingly
            if self._lifetime >= self.LIFETIME - self.SCALE_TIME:
                scale = self.SIZE * ((self.LIFETIME - self._lifetime) * 2)
                self.image = pygame.transform.scale(self._img, (scale, scale))
                self.rect = pygame.Rect(self._sposition.x - scale // 2,
                                        self._sposition.y - scale // 2,
                                        scale, scale)

            # If the lifetime is near the last SCALE TIME until 0
            # Animate to scale down and adjust the rect also
            if self._lifetime <= self.SCALE_TIME:
                scale = max(0, self.SIZE * (self._lifetime * 2))
                pos_mod = (self.SIZE - scale) // 2
                self.image = pygame.transform.scale(self._img, (scale, scale))
                self.rect = pygame.Rect(self._eposition.x + pos_mod,
                                        self._eposition.y + pos_mod,
                                        scale, scale)

            # If lifetime reaches 0 then change the spawn flag
            # Also we need to generate a new spawn delay count
            if self._lifetime == 0:
                self.spawned = False
                self._spawn_delay = self._generate_spawn_delay()

    def draw(self, screen):
        """ Draw the bomb in the screen if its spawned. """
        if self.spawned:
            screen.blit(self.image, self.rect)
