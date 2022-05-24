'''
interface scene
'''

import pygame

from .object_configs import ConfigManager
from .event_listener import EventListener


class Scene(EventListener):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.configs = config_manager

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass
