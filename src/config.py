"""
Config Class - config.py
--------------------------------------------------
This module contains the Global variables used
by the game as its configuration settings.
Every config can be accessed as a class attribute.
It also contains static methods for different
purposes like loading the assets.
--------------------------------------------------
Author: Fidel Jesus O. Surtida I
--------------------------------------------------
"""
from pathlib import Path
from enum import Enum


class GAMESTATE(Enum):
    """ Used for determining the current state of the game. """
    MENU = 0
    PLAY = 1
    GAMEOVER = 2


class Config:

    # SCREEN CONSTANTS
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # SNAKE CONSTANTS
    SNAKE_SPEED = 4
    SNAKE_SIZE = 40
    SNAKE_LIFETIME = 100

    # FOOD CONSTANTS
    FOOD_SIZE = 40
    FOOD_SPAWN_DELAY = 1000
    FOOD_BUFF_MIN_DELAY = 5000
    FOOD_BUFF_MAX_DELAY = 8000
    FOOD_BUFF_LIFETIME = 4

    # POWERUP CONSTANTS (SPEEDUP)
    BUFF_DURATION = 10
    SPEEDUP_SIZE = 60
    SPEEDUP_LIFETIME = 6
    SPEEDUP_MIN_DELAY = 7000
    SPEEDUP_MAX_DELAY = 10000

    # DEBUFF CONSTANTS (SLOWDOWN)
    SLOWDOWN_DURATION = 10
    SLOWDOWN_SIZE = 45
    SLOWDOWN_LIFETIME = 5
    SLOWDOWN_MIN_DELAY = 2000
    SLOWDOWN_MAX_DELAY = 5000

    # BASE PATH
    BASE_PATH = Path(__file__).resolve().parent.parent

    @classmethod
    def theme_path(cls):
        """ Returns the absolute theme path file. """
        return str(cls.BASE_PATH / "data/theme.json")

    @classmethod
    def assets_path(cls, filename=""):
        """ Returns the absolute assets path directory. """
        return str(cls.BASE_PATH / "assets") + f"/{filename}"
