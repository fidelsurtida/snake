import pygame
import random
from src.objects.food import Food
from src.config import Config


class FoodBuff(Food):

    # Class Event Constant
    SPAWN_FOOD_BUFF_EVENT = pygame.USEREVENT + 101

    def __init__(self, *, filename, points, regen):
        """
        Extends the Food class with additional animation sprite.
        This also randomizes the spawn time of the Food Buff by using
        the Config min and max delay stats.
        """
        super().__init__(filename=filename, points=points, regen=regen)
        self.spawn_event = self.SPAWN_FOOD_BUFF_EVENT

    def _trigger_spawn(self):
        """ Triggers the timer for the Food Buff to spawn. """
        delay = random.randint(Config.FOOD_BUFF_MIN_DELAY,
                               Config.FOOD_BUFF_MAX_DELAY)
        pygame.time.set_timer(self.SPAWN_FOOD_BUFF_EVENT, delay)
