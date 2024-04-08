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
import copy

# GLOBAL SETTINGS OF SNAKE
SPEED = 3
SIZE = 30


class Snake:
    # Movement Class Constants
    ZERO = pygame.Vector2(0, 0)
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
        self.tails = []
        for i in range(1, 4):
            self.body.append(SnakePart(posx, posy + SIZE * i,
                                       direction=Snake.UP, color="white"))

    def move(self, direction):
        """
        This will be called by the keyboard event in the Game Class.
        It will set the next movement of the head of the snake.
        """
        # Prevents the snake from moving to the opposite direction
        if self.direction + direction != Snake.ZERO:
            self.direction = direction
            self.head.next_movement(direction)

    def update(self):
        """
        On every update, if a part has moved twice its size, it will return
        the previous movement and pass it to the next part.
        This also appends a snake part as a tail if there are pending tails.
        """
        direction = self.head.update()
        for part in self.body:
            if direction:
                part.next_movement(direction)
            direction = part.update()

        # If there are pending tails, check first if it collides with current
        # last body part. If the last body part goes past this pending tail,
        # then teleport it to connect the edges and finally append it to the
        # body list.
        if self.tails:
            stem, tail = self.body[-1], self.tails[0]
            if not stem.bounds.colliderect(tail.bounds):
                if stem.direction == Snake.UP:
                    tail.teleport(*stem.bounds.bottomleft, corner="topleft")
                elif stem.direction == Snake.DOWN:
                    tail.teleport(*stem.bounds.topleft, corner="bottomleft")
                elif stem.direction == Snake.LEFT:
                    tail.teleport(*stem.bounds.bottomright, corner="bottomleft")
                elif stem.direction == Snake.RIGHT:
                    tail.teleport(*stem.bounds.bottomleft, corner="bottomright")

                tail.direction = stem.direction
                self.body.append(self.tails.pop(0))

    def draw(self, screen):
        """ Draws the snake parts with body first then lastly the head. """
        # Draws the Body Parts first.
        for part in self.body[::-1]:
            part.draw(screen)
        # Next draws the pending tails if there are any.
        for tail in self.tails:
            tail.draw(screen)

        # Next draws the Rectangle Covers for each turn of its body parts.
        snake = self.parts
        for i in range(len(snake) - 1):
            part1, part2 = snake[i:i+2]
            if part1.bounds.colliderect(part2.bounds):
                cover = part2.future_bounds
                pygame.draw.rect(screen, "gray", cover)

        # Lastly Draw the Head
        self.head.draw(screen)

    def grow(self):
        """
        To grow the snake, we need to copy the last part or the tail.
        We also stop this copied part's movement and append it to the
        queue of next tails.
        """
        last = copy.deepcopy(self.body[-1])
        last.stop()
        self.tails.append(last)

    @property
    def parts(self):
        """ Returns all the snake parts including the head. """
        return [self.head] + self.body

    @property
    def stretch(self):
        """ Gets the total stretch of the snake excluding the initial parts. """
        return (len(self.body) - 2) * SIZE // 10


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

    def teleport(self, x, y, *, corner="topleft"):
        """ Teleports the position of this snake part. """
        match corner:
            case "topleft": self._rect.topleft = (x, y)
            case "topright": self._rect.topright = (x, y)
            case "bottomleft": self._rect.bottomleft = (x, y)
            case "bottomright": self._rect.bottomright = (x, y)

    def stop(self):
        """ Stops the movement and next movement of this snake part. """
        self._movement = Snake.ZERO
        self._next_direction = Snake.ZERO

    @property
    def bounds(self):
        """ Returns the Rect or bounderies of this snake part. """
        return self._rect.copy()

    @property
    def direction(self):
        """ Returns the current movement of this snake part. """
        return self._movement

    @direction.setter
    def direction(self, value):
        """ Sets the current movement of this snake part. """
        self._movement = value

    @property
    def future_bounds(self):
        """
        Returns a Rect object of its future position based on movement.
        This will be used for generating the cover of the snake turn.
        """
        position = self._position + ((self._movement / SPEED) * SIZE)
        return pygame.Rect(position, (SIZE, SIZE))
