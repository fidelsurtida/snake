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

    def __init__(self, *, damage, deduction):
        """
        Initializes the bomb image as sprite and starts the countdown of
        the delay timer to spawn the bomb.
        """
        super().__init__()
        self.image = pygame.image.load(Config.assets_path("bomb.png"))
        self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))
        self.spawned = False
        self._spawn_delay = self._generate_spawn_delay()
        self._lifetime = self.LIFETIME
        self.damage = damage
        self.deduction = deduction
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
        rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        # Initialize the final valid position of this bomb object
        self.rect = rect
        self.spawned = True
        self._lifetime = self.LIFETIME

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
            # If lifetime reaches 0 then despawn the bomb and show explosion
            # Also we need to generate a new spawn delay count
            if self._lifetime == 0:
                self.spawned = False
                self._spawn_delay = self._generate_spawn_delay()

    def draw(self, screen):
        """ Draw the bomb in the screen if its spawned. """
        if self.spawned:
            screen.blit(self.image, self.rect)
