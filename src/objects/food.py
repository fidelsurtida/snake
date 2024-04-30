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
from src.objects.particles import ParticleSystem


class Food(Sprite):

    # Food Settings from Config
    SIZE = Config.FOOD_SIZE
    SPAWN_DELAY = Config.FOOD_SPAWN_DELAY

    # Class Event and Particle Sheet Constant
    SPAWN_FOOD_EVENT = pygame.USEREVENT + 100
    PARTICLE_SHEET = None

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

        # Create the Particle System for the Food
        assets_path = Config.assets_path("particles.png")
        Food.PARTICLE_SHEET = pygame.image.load(assets_path)
        health_particle = Food.PARTICLE_SHEET.subsurface(50, 0, 50, 50)
        self.particles = ParticleSystem(image=health_particle, size=18,
                                        lifetime=0.8, count=7)
        # Start the timer to spawn this Food Object after instantiation.
        self._trigger_spawn()

    def _trigger_spawn(self):
        """ Triggers the timer for the Food to spawn. """
        pygame.time.set_timer(self.SPAWN_FOOD_EVENT, self.SPAWN_DELAY)

    def spawn(self, *, off_limits_rects):
        """
        Sets the Food at a random position based on screen bounds.
        Spawn it not too close on the window borders and also there will
        be a GUI panel at the top with 50 height.
        We also need to check if the random position is not occupied by
        any of the passed rectangle off limits.
        """
        # Loop until a valid position is generated
        while True:
            x = random.randint(self.SIZE, self._swidth - self.SIZE * 2)
            y = random.randint(self.SIZE + 50, self._sheight - self.SIZE * 2)
            rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
            for off_limit in off_limits_rects:
                if off_limit and off_limit.colliderect(rect):
                    break
            else:
                break
        # Initialize the final valid position in this food object
        self.rect = rect
        self.spawned = True
        self.particles.spawn(self.rect)
        pygame.time.set_timer(self.spawn_event, 0)

    def update(self, time_delta):
        """ Updates the particle system of the Food. """
        self.particles.update(time_delta)

    def draw(self, screen):
        """
        Draws the Food to the screen only if spawned.
        Also draw the particle system whether spawned or not.
        """
        if self.spawned:
            screen.blit(self.image, self.rect)
        # Draw the particle system
        self.particles.draw(screen)

    def destroy(self):
        """
        Removes the Food Object on the screen by invalidating some properties.
        Also triggers the spawn timer for the next Food to spawn.
        """
        self.spawned = False
        self.rect = None
        self._trigger_spawn()
        # Trigger the destroy method of the particle system
        self.particles.destroy()

    @property
    def bounds(self):
        """ Returns the reduced Rect object of the Food. """
        rect = self.rect.copy()
        adjustment = self.SIZE // 4
        rect.topleft = (rect.x + adjustment, rect.y + adjustment)
        rect.size = (rect.width - adjustment * 2, rect.height - adjustment * 2)
        return rect

    @property
    def territory(self):
        """ Returns the expanded rect area of the food for off limits area. """
        if self.rect:
            rect = self.rect.copy()
            rect.topleft = (rect.x - self.SIZE, rect.y - self.SIZE)
            rect.size = (rect.width + self.SIZE * 2,
                         rect.height + self.SIZE * 2)
            return rect
