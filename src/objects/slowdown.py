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
from src.objects.snake import Snake
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

    def spawn_near_head(self, *, off_limits_rects, head):
        """
        This is a different version of the spawn from food class. It will
        spawn the slowdown debuff near the player snake head location.
        The logic will be the same except that the valid area will be smaller
        near the snake head and also should be clipped inside the window
        boundaries.
        """
        # Ready the required variables for location generation
        min_x, min_y = 40, 50
        area_x, area_y = 65, 65
        head_x, head_y = head.rect.topleft
        window_bounds = pygame.Rect(50, 60, self._swidth - min_x * 2,
                                    self._sheight - min_y * 2)
        # Based on head direction determine the correct front area
        range_x = (head_x - area_x // 2, head_x + area_x // 2)
        range_y = (head_y - area_y // 2, head_y + area_y // 2)
        match head.direction:
            case Snake.UP:
                range_y = (head_y - area_y - self.SIZE, head_y - self.SIZE)
            case Snake.DOWN:
                range_y = (head_y + self.SIZE, head_y + area_y + self.SIZE)
            case Snake.LEFT:
                range_x = (head_x - area_x - self.SIZE, head_x - self.SIZE)
            case Snake.RIGHT:
                range_x = (head_x + self.SIZE, head_x + area_x + self.SIZE)

        # Loop until a valid position is generated
        max_loop = 3
        while True:
            x = random.randint(*range_x)
            y = random.randint(*range_y)
            rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
            rect = rect.clamp(window_bounds)
            for off_limit in off_limits_rects:
                if off_limit and off_limit.colliderect(rect):
                    break
            else:
                break
            # If max loop reaches 0 then break this loop
            max_loop -= 1
            if max_loop <= 0:
                break

        # Initialize the final valid position in this food object
        # If maxloop reaches 0 then don't initialize the object
        if max_loop > 0:
            self.rect = rect
            self.spawned = True
            self.particles.spawn(self.rect)
            self.lifetime = self.LIFETIME_CONSTANT
            self.image.set_alpha(255)
            pygame.time.set_timer(self.spawn_event, 0)
        else:
            self._trigger_spawn()
