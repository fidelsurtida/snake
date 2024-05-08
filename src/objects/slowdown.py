"""
Slowdown Class - slowdown.py
-------------------------------------------------------
This module contains the SlowDown Class that extends
the FoodBuff Class. This is a debuff item that slows
the player snake to its minimum speed of 2. It will
dissappear after a set amount of time.
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


class SlowDown(FoodBuff):

    # Class Event Constant
    SPAWN_SLOW_DOWN_EVENT = pygame.USEREVENT + 103
    LIFETIME_CONSTANT = Config.SLOWDOWN_LIFETIME
    SIZE = Config.SLOWDOWN_SIZE

    def __init__(self, *, name, filename, points, value, negative):
        """
        Extends the FoodBuff class with additional slowdown attributes.
        """
        super().__init__(filename=filename, points=points, regen=0)
        self.spawn_event = self.SPAWN_SLOW_DOWN_EVENT
        self.lifetime = self.LIFETIME_CONSTANT
        self.value = value
        self.name = name
        self.negative = negative

        # Create the Particle System for the SpeedUp
        arrow_down = super().PARTICLE_SHEET.subsurface(150, 0, 50, 50)
        self.particles = ParticleSystem(image=arrow_down, size=28,
                                        lifetime=0.9, count=7,
                                        animation=Particle.TYPE.FALLING)

    def _trigger_spawn(self):
        """ Triggers the timer for the SpeedUp to spawn. """
        delay = random.randint(Config.SLOWDOWN_MIN_DELAY,
                               Config.SLOWDOWN_MAX_DELAY)
        pygame.time.set_timer(self.SPAWN_SLOW_DOWN_EVENT, delay)
