"""
FoodBuff Class - foodbuff.py
-----------------------------------------------------------
This module contains the FoodBuff Class that extends the
Food Class with additional particle sprite. This also
has a time limit before the Food Buff will disappear.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
import random
from src.objects.food import Food
from src.objects.particles import ParticleSystem
from src.config import Config


class FoodBuff(Food):

    # Class Event Constant
    SPAWN_FOOD_BUFF_EVENT = pygame.USEREVENT + 101

    def __init__(self, *, filename, points, regen):
        """
        Extends the Food class with additional animation sprite.
        This also randomizes the spawn time of the Food Buff by using
        the Config min and max delay stats.
        """
        super().__init__(filename=filename, points=points, regen=regen)
        self.spawn_event = self.SPAWN_FOOD_BUFF_EVENT
        self.lifetime = Config.FOOD_BUFF_LIFETIME
        # Create the Particle System for the Food Buff
        particle_sheet = pygame.image.load(Config.assets_path("particles.png"))
        shiny_image = particle_sheet.subsurface(0, 0, 50, 50)
        self.particles = ParticleSystem(image=shiny_image, size=25,
                                        lifetime=1, count=7)

    def _trigger_spawn(self):
        """ Triggers the timer for the Food Buff to spawn. """
        delay = random.randint(Config.FOOD_BUFF_MIN_DELAY,
                               Config.FOOD_BUFF_MAX_DELAY)
        pygame.time.set_timer(self.SPAWN_FOOD_BUFF_EVENT, delay)

    def spawn(self, *, off_limits):
        """
        Draw first the food buff image by calling the super class method.
        Then spawn the particle effect of the food buff.
        """
        super().spawn(off_limits=off_limits)
        self.particles.spawn(self.rect)
        self.lifetime = Config.FOOD_BUFF_LIFETIME
        self.image.set_alpha(255)

    def update(self, time_delta):
        """
        Updates the particle animation of the Food Buff.
        This will also reduce the lifetime of food buff and
        automatically destroys itself when lifetime reaches 0.
        """
        self.particles.update(time_delta)
        if self.spawned:
            # Update the lifetime of the Food Buff
            self.lifetime = max(0, self.lifetime - time_delta)
            # Update the alpha value of the Food Buff image
            # Delay the alpha reduction by half of the lifetime
            if self.lifetime <= Config.FOOD_BUFF_LIFETIME / 2:
                alpha = self.lifetime / (Config.FOOD_BUFF_LIFETIME / 2) * 255
                self.image.set_alpha(alpha)
            # Destory the Food Buff if lifetime reaches 0
            if self.lifetime <= 0:
                self.destroy()

    def draw(self, screen):
        """ Draws the Food Buff and its particle animation. """
        super().draw(screen)
        self.particles.draw(screen)

    def destroy(self):
        """ Releases the Food Buff and its particle animation. """
        super().destroy()
        self.particles.destroy()
