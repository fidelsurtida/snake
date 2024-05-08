"""
SpeedUp Class - speedup.py
-------------------------------------------------------
This module contains the SpeedUp Class that extends
the FoodBuff Class. This is a type of Item Buff that
adds a temporary speed boost to the movement of the
snake when eaten. It inherits the dissapearance effect
of the food buff after a set amount of time.
-------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-------------------------------------------------------
"""
import pygame
import random
from src.objects.foodbuff import FoodBuff
from src.objects.particles import Particle
from src.objects.particles import ParticleSystem
from src.config import Config


class SpeedUp(FoodBuff):

    # Class Event Constant
    SPAWN_SPEED_UP_EVENT = pygame.USEREVENT + 102
    LIFETIME_CONSTANT = Config.SPEEDUP_LIFETIME
    SIZE = Config.SPEEDUP_SIZE

    def __init__(self, *, name, filename, points, value, negative):
        """
        Extends the FoodBuff class with additional speed attributes.
        """
        super().__init__(filename=filename, points=points, regen=0)
        self.spawn_event = self.SPAWN_SPEED_UP_EVENT
        self.lifetime = self.LIFETIME_CONSTANT
        self.value = value
        self.name = name
        self.negative = negative

        # Create the Particle System for the SpeedUp
        arrow_up = super().PARTICLE_SHEET.subsurface(100, 0, 50, 50)
        self.particles = ParticleSystem(image=arrow_up, size=28,
                                        lifetime=0.8, count=6,
                                        animation=Particle.TYPE.FLOATING)

    def _trigger_spawn(self):
        """ Triggers the timer for the SpeedUp to spawn. """
        delay = random.randint(Config.SPEEDUP_MIN_DELAY,
                               Config.SPEEDUP_MAX_DELAY)
        pygame.time.set_timer(self.SPAWN_SPEED_UP_EVENT, delay)