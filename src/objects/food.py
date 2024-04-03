"""
Food Class - food.py
-----------------------------------------------------
This module contains the Food Class that will spawn
the food that the snake will eat for it to grow.
It will be spawned randomly and on a specific spot
on the screen that has not been occupied by any
snake part.
-----------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------
"""
import pygame
import random

# GLOBAL SETTINGS OF THE FOOD
SIZE = 20
SPAWN_DELAY = 1000


class Food:
    # Class Constants
    SPAWN_FOOD_EVENT = pygame.USEREVENT + 1

    def __init__(self, *, screen_width, screen_height):
        """
        Initializes a red Food Object with its given size. At first, it will
        start as unspawned and will be triggered to spawn after a delay.
        This also accepts the screen width and height to determine the
        random position of the Food.
        """
        self.color = "red"
        self.spawned = False
        self._swidth = screen_width
        self._sheight = screen_height
        self._rect = None
        # Start the timer to spawn this Food Object after instantiation.
        self._trigger_spawn()

    def _trigger_spawn(self):
        """ Triggers the timer for the Food to spawn. """
        pygame.time.set_timer(self.SPAWN_FOOD_EVENT, SPAWN_DELAY)

    def spawn(self):
        """ Sets the Food at a random position based on screen bounds. """
        x = random.randint(0, self._swidth - SIZE)
        y = random.randint(0, self._sheight - SIZE)
        self._rect = pygame.Rect(x, y, SIZE, SIZE)
        self.spawned = True
        pygame.time.set_timer(self.SPAWN_FOOD_EVENT, 0)

    def destroy(self):
        """
        Removes the Food Object on the screen by invalidating some properties.
        Also triggers the spawn timer for the next Food to spawn.
        """
        self.spawned = False
        self._rect = None
        self._trigger_spawn()

    def draw(self, screen):
        """ Draws the Food to the screen only if spawned. """
        if self.spawned:
            pygame.draw.rect(screen, self.color, self._rect)

    @property
    def bounds(self):
        """ Returns the Rect object of the Food. """
        return self._rect.copy()
