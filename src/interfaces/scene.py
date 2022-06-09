'''
interface scene
'''

import pygame

from .event_listener import EventListener


class Scene(EventListener):
    def __init__(self):
        super().__init__()

    def start_scene(self):
        pass

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        pass
