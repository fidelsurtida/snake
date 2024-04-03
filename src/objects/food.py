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


class Food:
    def __init__(self):
        self.color = "red"
        self.bounds = pygame.Rect(0, 0, SIZE, SIZE)

    def spawn(self, screen_bounds: pygame.Rect):
        """ Sets the Food at a random position based on screen bounds. """
        swidth, sheight = screen_bounds.size
        x = random.randint(0, swidth - SIZE)
        y = random.randint(0, sheight - SIZE)
        self.bounds.topleft = (x, y)

    def draw(self, screen):
        """ Draws the Food to the screen. """
        pygame.draw.rect(screen, self.color, self.bounds)
