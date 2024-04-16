"""
Floater Class - floater.py
-----------------------------------------------------------
This module contains the Floater Class that encapsulates
the UILabel and an Image as an icon that will float up
when spawned and fades out as it goes up.
This module can be used for displaying attained points on
food and also other messages for different powerups.
-----------------------------------------------------------
Author: Fidel Jesus O. Surtida I
-----------------------------------------------------------
"""
import pygame
import pygame_gui


class Floater:

    def __init__(self, *, name, position, dimension, text, icon, isize):
        """
        Initialize a UILabel from the pygame_ui as text label on the left.
        The icon image will be resized and placed on the right side.
        """
        x, y, (width, height) = position.x, position.y - 30, dimension
        x -= (width + isize) / 3
        icon_y = y + ((height - isize) / 2) + 2
        icon = pygame.transform.scale(icon, (isize, isize))

        self._icon = icon
        self._icon_rect = pygame.Rect(x + width, icon_y, isize, isize)
        self._label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(x, y, width, height),
            text=text, object_id=f"@{name}_lbl"
        )
        # Activate the fade text effect for the label to start animation
        self._label.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT,
                                      {"time_per_alpha_change": 6})

    @property
    def label(self):
        """ Returns the UILabel object for this floater. """
        return self._label

    def draw(self, screen):
        """ Draws the icon to the screen. """
        screen.blit(self._icon, self._icon_rect)

    def update(self):
        """ Updates the movement of label and icon to float going up. """
        x, y = self._label.rect.topleft
        self._label.set_relative_position((x, y - 1))
        self._icon_rect.move_ip(0, -1)
        # We also need to update the alpha value of the icon
        self._icon.set_alpha(self._icon.get_alpha() - 3)

    def destroy(self):
        """ Releases the label and icon from the memory. """
        self._label.kill()
        del self._label
        del self._icon
        del self._icon_rect
