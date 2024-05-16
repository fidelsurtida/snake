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
import pygame_gui
import copy
from pygame.sprite import Sprite
from src.config import Config


class Snake:

    # Snake Settings from Config
    SPEED = Config.SNAKE_SPEED
    SIZE = Config.SNAKE_SIZE
    LIFETIME = Config.SNAKE_LIFETIME
    BUFF_DURATION = Config.BUFF_DURATION

    # Movement Class Constants
    ZERO = pygame.Vector2(0, 0)
    UP = pygame.Vector2(0, -SPEED)
    DOWN = pygame.Vector2(0, SPEED)
    LEFT = pygame.Vector2(-SPEED, 0)
    RIGHT = pygame.Vector2(SPEED, 0)

    def __init__(self, *, background=None, posx=512, posy=384):
        """
        Initialize a Snake object with a head and a list of body parts
        This will be placed in the center of screen with initial movement
        of going up.
        These also accepts a background image to be saved in order for
        the curve covers to completely hide the moving parts underneath.
        """
        # Save the background image as an attribute
        self.bg = background
        # Load the Snake Sprite and seperate the parts
        self._load_snake_parts()

        # Snake Variables
        self._locked_direction = False
        self._head_index = 0
        self._time_frame = 0
        self.direction = Snake.UP
        self.head = SnakePart(posx, posy, direction=Snake.UP,
                              image=self._headimg[self._head_index])
        self.body = []
        self.tails = []
        self.covers = []
        self.lifetime = Snake.LIFETIME
        self.dead = False
        self.buff_icon = None
        self._old_tail_direction = None
        self._buff_duration = 0
        self._buff_counter = None
        self._buff_rect = None
        for i in range(1, 5):
            # Seperate the tail sprite into the last element
            sprite = self._bodyimg if i < 4 else self._tailimg
            self.body.append(SnakePart(posx, posy + Snake.SIZE * i,
                                       direction=Snake.UP, image=sprite))

    def _load_snake_parts(self):
        """
        Loads the snake sprite parts from the snake sprite sheet.
        It also resizes the covers to the correct snake size config.
        """
        # Load the main snake sprite sheet
        snake_sheet = pygame.image.load(Config.assets_path("snake.png"))
        # Get the head animation sprite images
        self._headimg = [
            snake_sheet.subsurface((1, 1, 40, 42)),
            snake_sheet.subsurface((1, 45, 40, 40)),
            snake_sheet.subsurface((1, 85, 40, 40))
        ]
        self._dead_headimg = snake_sheet.subsurface((1, 126, 40, 39))
        self._bodyimg = snake_sheet.subsurface((85, 85, 40, 40))
        self._tailimg = snake_sheet.subsurface((43, 85, 40, 40))
        # Get the 4 different turn parts image
        surfaces = [
            snake_sheet.subsurface((43, 1, 40, 40)),   # TOPLEFT
            snake_sheet.subsurface((85, 1, 40, 40)),   # TOPRIGHT
            snake_sheet.subsurface((43, 43, 40, 40)),  # BOTTOMLEFT
            snake_sheet.subsurface((85, 43, 40, 40))   # BOTTOMRIGHT
        ]
        # Resize the covers to correct body size
        for i, sur in enumerate(surfaces):
            surfaces[i] = pygame.transform.scale(sur, (Snake.SIZE, Snake.SIZE))
        # Finally assign the covers to the class attributes
        self._topleft_cover, self._topright_cover = surfaces[:2]
        self._bottomleft_cover, self._bottomright_cover = surfaces[2:]

    def move(self, direction):
        """
        This will be called by the keyboard event in the Game Class.
        It will set the next movement of the head of the snake.
        """
        # Prevents the snake from moving to the opposite direction
        # Also once this move is given, lock movement change until
        # the snake part has moved twice its size.
        if not self._locked_direction:
            if self.direction + direction != Snake.ZERO:
                self.direction = direction
                self.head.next_movement(direction)
                self._locked_direction = True

    def update(self, time_delta):
        """
        On every update, if a part has moved twice its size, it will return
        the previous movement and pass it to the next part.
        This also appends a snake part as a tail if there are pending tails.
        This also calls the helper method to create snake covers for each
        turning part of the snake. Updates also the delay of each cover.
        """
        direction = self.head.update()
        # Unlock the movement change if the head returned a direction
        if direction is not None:
            self._locked_direction = False
        # Proceed to propagate the movement direction to the rest of body.
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

        # Calls the helper method that creates the turn covers of the snake.
        # Updates the existing covers to reduce the delay counter.
        self._create_turn_covers()
        for cover in self.covers[:]:
            if cover.update(time_delta):
                self.covers.remove(cover)

        # Updates the head sprite animation index
        self._time_frame += time_delta
        if not self.dead and self._time_frame > 0.08:
            self._head_index = (self._head_index + 1) % 3
            self.head.change_sprite(self._headimg[self._head_index])
            self._time_frame = 0

        # Updates the buff duration and buff icon alpha value
        if self._buff_duration > 0:
            alpha = 255
            # Update the duration, alpha value based on duration left
            self._buff_duration -= time_delta
            # Update the alpha only in last 3 seconds of the buff duration
            if self._buff_duration <= 3:
                alpha = max(0, int(self._buff_duration / 3 * 255))
            self.buff_icon.set_alpha(alpha)
            # Create the Buff Rect as a reference for the Buff Counter
            self._buff_rect = self.head.rect.copy()
            self._buff_rect.move_ip(-5, -33)
            text_rect = self._buff_rect.copy()
            text_rect.move_ip(15, -5)
            # Apply position to the buff counter label and set the alpha
            self._buff_counter.set_position(text_rect)
            self._buff_counter.set_text(f"{round(self._buff_duration):.0f}")
            self._buff_counter.set_text_alpha(alpha)
        # If buff duration reaches 0 then remove the buff icon
        elif self._buff_duration <= 0:
            # Reset the buff attributes and snake speed
            if self._buff_counter:
                self.set_snake_speed(Config.SNAKE_SPEED)
                self._buff_counter.kill()
                self._buff_counter = None
            self.buff_icon = None
            self._buff_rect = None

    def draw(self, screen):
        """ Draws the snake parts with body first then lastly the head. """
        # Draws the Body Parts first.
        for part in self.body:
            part.draw(screen)

        # Next draws the pending tails if there are any.
        for tail in self.tails:
            tail.draw(screen)

        # Next draws the Curve Covers for each turn of its body parts.
        for cover in self.covers:
            cover.draw(screen)

        # Lastly Draw the Head
        self.head.draw(screen)

        # Draw the Buff Icon if there is a buff applied
        if self.buff_icon:
            screen.blit(self.buff_icon, self._buff_rect)

    def _create_turn_covers(self):
        """
        Creates a SnakeCover object for each turning part of the snake.
        This will be called in the update method to create covers list.
        This contains a helper method to determine the type of cover.
        """
        def get_cover(*parts):
            first_dir, second_dir = parts[0].direction, parts[1].direction
            match (first_dir, second_dir):
                case (Snake.DOWN, Snake.RIGHT) | (Snake.LEFT, Snake.UP):
                    return self._topright_cover
                case (Snake.RIGHT, Snake.UP) | (Snake.DOWN, Snake.LEFT):
                    return self._topleft_cover
                case (Snake.RIGHT, Snake.DOWN) | (Snake.UP, Snake.LEFT):
                    return self._bottomleft_cover
                case (Snake.LEFT, Snake.DOWN) | (Snake.UP, Snake.RIGHT):
                    return self._bottomright_cover

        # Check first if subsequent parts collide with each other
        # Create a Snake Cover if it does not exist in covers list
        for i in range(len(self.parts) - 1):
            first, second = self.parts[i:i+2]
            if first.bounds.colliderect(second.bounds):
                cover_rect = second.future_bounds
                existing = [c for c in self.covers if c.rect == cover_rect]
                # If future_bounds is not found in current covers, create one
                if not existing:
                    turn_cover = get_cover(first, second)
                    if turn_cover:
                        self.covers.append(SnakeCover(cover_rect, turn_cover,
                                           self.bg, second.direction))
                else:
                    # If it exists, reset the delay counter
                    existing[0].reset_delay()

        # Check the last part of the body and the pending tail if it needs
        # to refresh / reset delay an existing cover.
        if self.tails:
            first, second = self.body[-1], self.tails[0]
            if first.bounds.colliderect(second.bounds):
                second.direction = self._old_tail_direction
                cover_rect = second.future_bounds
                second.direction = Snake.ZERO
                existing = [c for c in self.covers if c.rect == cover_rect]
                if existing:
                    existing[0].reset_delay()

    def grow(self):
        """
        To grow the snake, we need to copy the last part or the tail.
        We also stop this copied part's movement and append it to the
        queue of next tails.
        """
        last = copy.deepcopy(self.body[-1])
        self._old_tail_direction = last.direction
        last.stop()
        self.tails.append(last)
        # Change the last element of body to body sprite
        # And update the new tail to its new sprite tail image
        self.body[-1].change_sprite(self._bodyimg)
        last.change_sprite(self._tailimg, self.body[-1].direction)

    def apply_buff(self, buff):
        """
        Applies the buff to the snake. Get the image of buff item.
        Determine the effect based on the value of the buff and the
        name of the buff.
        """
        self._buff_duration = self.BUFF_DURATION

        if self._buff_counter:
            self._buff_counter.kill()
            self._buff_counter = None

        if buff.name == "speedup":
            # Change the snake speed and constants
            self.set_snake_speed(buff.value)
            # Set the icon and create the buff label counter
            self.buff_icon = pygame.transform.scale(buff.image, (28, 28))
            self._buff_counter = pygame_gui.elements.UILabel(
                relative_rect=self.head.rect, text=f"{self.BUFF_DURATION}"
            )
        elif buff.name == "slowdown":
            # Change the snake speed and constants
            self.set_snake_speed(buff.value)
            # Set the icon and create the buff label counter
            self.buff_icon = pygame.transform.scale(buff.image, (28, 28))
            self._buff_counter = pygame_gui.elements.UILabel(
                relative_rect=self.head.rect, text=f"{self.BUFF_DURATION}"
            )

    def set_snake_speed(self, speed):
        """ Updates the speed of the Snake object and Class constants. """
        # Change the part speed based on the buff value
        for part in self.parts:
            part.set_speed(speed)
        # Update the Snake class speed constants
        Snake.SPEED = speed
        Snake.UP = pygame.Vector2(0, -speed)
        Snake.DOWN = pygame.Vector2(0, speed)
        Snake.LEFT = pygame.Vector2(-speed, 0)
        Snake.RIGHT = pygame.Vector2(speed, 0)

    def die(self):
        """ Changes the sprite of the head of snake to dead sprite. """
        self.dead = True
        self.head.change_sprite(self._dead_headimg, self.direction)
        # Remove the buff counter if available
        if self._buff_counter:
            self.set_snake_speed(Config.SNAKE_SPEED)
            self._buff_counter.kill()

    @property
    def parts(self):
        """ Returns all the snake parts including the head. """
        return [self.head] + self.body

    @property
    def rects(self):
        """ Returns all the snake part rects including the head. """
        return [part.bounds for part in self.parts]

    @property
    def stretch(self):
        """ Gets the total stretch of the snake excluding the initial parts. """
        return len(self.body) - 3


class SnakePart(Sprite):

    def __init__(self, posx, posy, *, direction, image):
        """
        Initializes a SnakePart object with position to tract its old position.
        It has a Rect object to draw the part on the screen.
        It has a movement Vector2 which is the current movement of the part.
        And the next_direction is the next movement of the part
        after it moves twice its size.
        """
        super().__init__()
        self._position = pygame.Vector2(posx - Snake.SIZE // 2,
                                        posy - Snake.SIZE // 2)
        self._next_direction = direction
        self._movement = direction
        self.rect = pygame.Rect(self._position.x, self._position.y,
                                Snake.SIZE, Snake.SIZE)
        self._future_position = self.future_bounds.topleft
        # Save 2 images, the original _img is used for correctly rotating
        self.image = pygame.transform.scale(image, (Snake.SIZE, Snake.SIZE))
        self._img = image
        self._normalize_sprite()

    def next_movement(self, direction):
        """
        This will be called by the move method of the Snake class to set the
        next movement of the head.
        Also, this will be called by the update method to set the next movement
        of the part after it moves twice its size.
        """
        self._next_direction = direction

    def update(self) -> pygame.Vector2 | None:
        """
        This moves the part based on the saved movement Vector2.
        If this part has moved twice its size, it will return the previous
        movement so that it will be passed to the next part in the list.
        Its next movement also will be set based on the passed velocity.
        """
        if (
            abs(self.rect.x - self._position.x) >= Snake.SIZE or
            abs(self.rect.y - self._position.y) >= Snake.SIZE
        ):
            old_direction = self._movement
            self._movement = self._next_direction
            self.rect.topleft = self._future_position
            self._position = pygame.Vector2(self.rect.x, self.rect.y)
            self._future_position = self.future_bounds.topleft
            self.rect.move_ip(self._movement.x, self._movement.y)
            self._normalize_sprite()
            return old_direction

        self.rect.move_ip(self._movement.x, self._movement.y)

    def draw(self, screen):
        """ Draw this individual part to the screen. """
        screen.blit(self.image, self.rect)

    def teleport(self, x, y, *, corner="topleft"):
        """ Teleports the position of this snake part. """
        match corner:
            case "topleft": self.rect.topleft = (x, y)
            case "topright": self.rect.topright = (x, y)
            case "bottomleft": self.rect.bottomleft = (x, y)
            case "bottomright": self.rect.bottomright = (x, y)

    def set_speed(self, speed):
        """ Sets the new speed of the next direction and current movement. """
        self._movement = self._movement / Snake.SPEED * speed
        self._next_direction = self._next_direction / Snake.SPEED * speed

    def stop(self):
        """ Stops the movement and next movement of this snake part. """
        self._movement = Snake.ZERO
        self._next_direction = Snake.ZERO

    def change_sprite(self, sprite, direction=None):
        """ Updates the original image and the sprite image attribute. """
        self._img = sprite
        self.image = sprite
        self._normalize_sprite(direction)

    @property
    def bounds(self):
        """ Returns the Rect or bounderies of this snake part. """
        return self.rect.copy()

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
        position = self._position + (self._movement / Snake.SPEED * Snake.SIZE)
        return pygame.Rect(position, (Snake.SIZE, Snake.SIZE))

    def _normalize_sprite(self, direction=None):
        """ Rotates the sprite image based on the direction."""
        if self.image:
            # Normalize the direction to the correct speed
            if direction:
                divisor = max(abs(direction.x), abs(direction.y))
                direction = direction / divisor * Snake.SPEED
            # Determine the correct sprite orientation
            index = direction or self._movement
            directions = [Snake.ZERO, Snake.DOWN, Snake.UP,
                          Snake.LEFT, Snake.RIGHT]
            degrees = [0, 0, 180, -90, 90][directions.index(index)]
            self.image = pygame.transform.rotate(self._img, degrees)


class SnakeCover:

    def __init__(self, cover_rect, turn_cover, background=None, direction=None):
        """
        Initializes a SnakeCover object to cover the turning snake parts.
        It has a delay counter that determines the lifetime of the cover.
        """
        self._turn_cover = turn_cover
        self.rect = cover_rect
        self.bg_rect = cover_rect.copy()
        self.delay = 0.07
        # Create a new rect for the bgcover to adjust and subsurface it to bg
        adjustment = direction / Snake.SPEED * 7
        match direction:
            case Snake.DOWN | Snake.RIGHT:
                self.bg_rect.size += adjustment
            case Snake.UP | Snake.LEFT:
                self.bg_rect.topleft += adjustment
                self.bg_rect.size -= adjustment
        self._bg_cover = background.subsurface(self.bg_rect)

    def draw(self, screen):
        """ Draw first the bg_cover then next is the turn_cover. """
        if self._bg_cover:
            screen.blit(self._bg_cover, self.bg_rect)
        screen.blit(self._turn_cover, self.rect)

    def update(self, time_delta):
        """ Reduces the delay counter based on passed time_delta. """
        self.delay -= time_delta
        return True if self.delay <= 0 else False

    def reset_delay(self):
        """ Resets the delay counter to its initial value. """
        self.delay = 0.07
