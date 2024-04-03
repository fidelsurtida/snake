"""
Snake Class / SnakePart Class - snake.py
-----------------------------------------------------------
This module contains the Snake Class that encapsulates the
SnakePart Objects to form the player as a snake game object.
It has a main part (the head) which controls the initial
movement and a list of body parts that follows the head.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame

# GLOBAL SETTINGS OF SNAKE
SPEED = 3
SIZE = 30


class Snake:
    # Movement Class Constants
    UP = pygame.Vector2(0, -SPEED)
    DOWN = pygame.Vector2(0, SPEED)
    LEFT = pygame.Vector2(-SPEED, 0)
    RIGHT = pygame.Vector2(SPEED, 0)

    def __init__(self, *, posx=512, posy=384):
        """
        Initialize a Snake object with a head and a list of body parts
        This will be placed in the center of screen with initial movement
        of going up.
        """
        self.direction = Snake.UP
        self.head = SnakePart(posx, posy, direction=Snake.UP, color="green")
        self.body = []
        for i in range(1, 4):
            self.body.append(SnakePart(posx, posy + SIZE * i,
                                       direction=Snake.UP, color="white"))

    def move(self, direction):
        """
        This will be called by the keyboard event in the Game Class.
        It will set the next movement of the head of the snake.
        """
        # Prevents the snake from moving to the opposite direction
        if self.direction + direction != pygame.Vector2(0, 0):
            self.direction = direction
            self.head.next_movement(direction)

    def update(self):
        """
        On every update, if a part has moved twice its size, it will return
        the previous movement and pass it to the next part.
        """
        direction = self.head.update()
        for part in self.body:
            if direction:
                part.next_movement(direction)
            direction = part.update()

    def draw(self, screen):
        """ Draws the snake parts with body first then lastly the head. """
        # Draws the Body Parts first.
        for part in self.body[::-1]:
            part.draw(screen)

        # Next draws the Rectangle Covers for each turn of its body parts.
        snake = self.parts
        for i in range(len(snake) - 1):
            part1 = snake[i].bounds
            part2 = snake[i+1].bounds
            if part1.colliderect(part2):
                cover = snake[i+1].future_bounds
                pygame.draw.rect(screen, "gray", cover)

        # Lastly Draw the Head
        self.head.draw(screen)

    @property
    def parts(self):
        """ Returns all the snake parts including the head. """
        return [self.head] + self.body


class SnakePart:
    def __init__(self, posx, posy, *, direction, color):
        """
        Initializes a SnakePart object with position to tract its old position.
        It has a Rect object to draw the part on the screen.
        It has a movement Vector2 which is the current movement of the part.
        And the next_direction is the next movement of the part
        after it moves twice its size.
        """
        self._position = pygame.Vector2(posx - SIZE//2, posy - SIZE//2)
        self._next_direction = direction
        self._movement = direction
        self._color = color
        self._rect = pygame.Rect(self._position.x, self._position.y, SIZE, SIZE)

    def next_movement(self, direction):
        """
        This will be called by the move method of the Snake class to set the
        next movement of the head.
        Also, this will be called by the update method to set the next movement
        of the part after it moves twice its size.
        """
        self._next_direction = direction

    def update(self):
        """
        This moves the part based on the saved movement Vector2.
        If this part has moved twice its size, it will return the previous
        movement so that it will be passed to the next part in the list.
        Its next movement also will be set based on the passed velocity.
        """
        old_direction = None
        if (
            abs(self._rect.x - self._position.x) >= SIZE or
            abs(self._rect.y - self._position.y) >= SIZE
        ):
            old_direction = self._movement
            self._movement = self._next_direction
            self._position = pygame.Vector2(self._rect.x, self._rect.y)

        self._rect.move_ip(self._movement.x, self._movement.y)
        return old_direction

    def draw(self, screen):
        """ Draw this individual part to the screen. """
        pygame.draw.rect(screen, self._color, self._rect)

    @property
    def bounds(self):
        """ Returns the Rect or bounderies of this snake part. """
        return self._rect.copy()

    def teleport(self, x, y):
        """ Teleports the position of this snake part. """
        self._rect.topleft = (x, y)

    @property
    def future_bounds(self):
        """
        Returns a Rect object of its future position based on movement.
        This will be used for generating the cover of the snake turn.
        """
        position = self._position + ((self._movement / SPEED) * SIZE)
        return pygame.Rect(position, (SIZE, SIZE))
