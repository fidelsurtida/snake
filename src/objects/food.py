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
from pygame.sprite import Sprite
from src.config import Config


class Food(Sprite):

    # Food Settings from Config
    SIZE = Config.FOOD_SIZE
    SPAWN_DELAY = Config.FOOD_SPAWN_DELAY

    # Class Event Constant
    SPAWN_FOOD_EVENT = pygame.USEREVENT + 100

    def __init__(self, *, filename, points, regen):
        """
        Initializes a red Food Object with its given size. At first, it will
        start as unspawned and will be triggered to spawn after a delay.
        This also accepts the screen width and height to determine the
        random position of the Food.
        """
        super().__init__()
        self.image = pygame.image.load(Config.assets_path(filename))
        self.image = pygame.transform.scale(self.image, (self.SIZE, self.SIZE))
        self.spawned = False
        self.spawn_event = self.SPAWN_FOOD_EVENT
        self.points = points
        self.regen = regen
        self._swidth = Config.SCREEN_WIDTH
        self._sheight = Config.SCREEN_HEIGHT
        # Start the timer to spawn this Food Object after instantiation.
        self._trigger_spawn()

    def _trigger_spawn(self):
        """ Triggers the timer for the Food to spawn. """
        pygame.time.set_timer(self.SPAWN_FOOD_EVENT, self.SPAWN_DELAY)

    def spawn(self, *, off_limits):
        """
        Sets the Food at a random position based on screen bounds.
        Spawn it not too close on the window borders and also there will
        be a GUI panel at the top with 50 height.
        We also need to check if the random position is not occupied by
        any of the snake parts.
        """
        # Loop until a valid position is generated
        while True:
            x = random.randint(self.SIZE, self._swidth - self.SIZE * 2)
            y = random.randint(self.SIZE + 50, self._sheight - self.SIZE * 2)
            rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
            for part in off_limits:
                if part.bounds.colliderect(rect):
                    break
            else:
                break
        # Initialize the final valid position in this food object
        self.rect = rect
        self.spawned = True
        pygame.time.set_timer(self.spawn_event, 0)

    def destroy(self):
        """
        Removes the Food Object on the screen by invalidating some properties.
        Also triggers the spawn timer for the next Food to spawn.
        """
        self.spawned = False
        self.rect = None
        self._trigger_spawn()

    def draw(self, screen):
        """ Draws the Food to the screen only if spawned. """
        if self.spawned:
            screen.blit(self.image, self.rect)

    @property
    def bounds(self):
        """ Returns the Rect object of the Food. """
        return self.rect.copy()
