"""
Particle Class / ParticleSystem Class - particles.py
-----------------------------------------------------------
These modules contains the Particle Class that is used
to represent a single image particle that is respawned on
a given area. It resizes the image from small to big and
vice versa as it reaches its lifetime.
The ParticleSystem Class is used to manage multiple
particles.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
import random


class Particle:

    def __init__(self, *, image, spawn_rect, size, lifetime):
        """
        Initializes a single particle object with its image,
        spawn area, max size and max lifetime. This will be used
        by the particle system to create multiple particles.
        """
        self.image = image
        self.rect = None
        self.spawn_area = spawn_rect
        self.lifetime = lifetime
        self.size = size
        # Internal variables for particle animation
        self._position = None
        self._lifetimer = 0
        self._scaledimg = None
        self._delay = 0
        self._stopping = False
        self._stopped = False
        # Once instantiated, call the spawn method
        self._spawn()

    def _spawn(self):
        """ Spawns the particle with initial values and random location. """
        x = random.randint(self.spawn_area.left, self.spawn_area.right)
        y = random.randint(self.spawn_area.top, self.spawn_area.bottom)
        self._position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x, y, 1, 1)
        self._scaledimg = pygame.transform.scale(self.image, (1, 1))
        self._lifetimer = 0
        self._delay = random.random() * 1.5

    def update(self, time_delta):
        """
        Updates the particle size and lifetimer. The first half of the
        lifetime we should increase the size to max size. The second half
        will be used to reduce the size to 0.
        """
        # Update first the delay timer to prevent immediate spawn
        self._delay = max(0, self._delay - time_delta)
        if self._delay > 0 or self._stopped:
            return

        # Increase the lifetimer until it reaches the lifetime
        # Else respawn the particle to its initial state and diff location
        if self._lifetimer <= self.lifetime:
            self._lifetimer += time_delta
        else:
            self._spawn() if not self._stopping else self._stop()

        # Increase the size first in the first half of its lifetime
        halftime, size = self.lifetime / 2, 0
        if self._lifetimer < self.lifetime / 2:
            size = int(self.size * (self._lifetimer / halftime))
        elif self._lifetimer >= self.lifetime / 2:
            size = int(self.size * (self._lifetimer / self.lifetime))
            size = self.size - size

        # Update the rect and resize the image based on determined size
        self.rect = pygame.Rect(self._position.x - size // 2,
                                self._position.y - size // 2, size, size)
        self._scaledimg = pygame.transform.scale(self.image, self.rect.size)

    def draw(self, screen):
        """ Draws this particle if lifetime is greater than 0. """
        if not self._stopped:
            if self._delay <= 0 and self._lifetimer < self.lifetime:
                screen.blit(self._scaledimg, self.rect)

    def stop(self):
        """ Sets the flag to destroy this particle. """
        self._stopping = True

    def _stop(self):
        """ Sets the final stop flag to stop this particle. """
        self._stopped = True


class ParticleSystem:

    def __init__(self, *, image, size, lifetime, count):
        """
        Creates a list of Particle objects and initializes them
        based on the given parameters.
        """
        self.particles = None
        self._image = image
        self._size = size
        self._lifetime = lifetime
        self._count = count

    def spawn(self, area):
        """ Initializes the particles based on the count. """
        self.particles = [Particle(image=self._image, spawn_rect=area,
                                   size=self._size, lifetime=self._lifetime)
                          for _ in range(self._count)]

    def update(self, time_delta):
        """ Updates each particle in this system. """
        if self.particles:
            for particle in self.particles:
                particle.update(time_delta)

    def draw(self, screen):
        """ Draws each particle in this system. """
        if self.particles:
            for particle in self.particles:
                particle.draw(screen)

    def destroy(self):
        """ Stops and destroys each particle in this system. """
        for particle in self.particles:
            particle.stop()
