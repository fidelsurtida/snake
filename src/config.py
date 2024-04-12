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


class Config:

    # SCREEN CONSTANTS
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # SNAKE CONSTANTS
    SNAKE_SPEED = 3
    SNAKE_SIZE = 30
    SNAKE_LIFETIME = 100

    # FOOD CONSTANTS
    FOOD_SIZE = 40
    FOOD_SPAWN_DELAY = 1000

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
