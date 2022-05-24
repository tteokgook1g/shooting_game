'''
class SceneManager
'''

import pygame

from ..interfaces.scene import Scene
from ..interfaces.event_listener import EventListener
from ..interfaces.object_configs import ConfigManager


class SceneManager(EventListener):
    def __init__(self, config_manager: ConfigManager):
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene = None
        self.next_scene: Scene = None
        self.config_manager = config_manager

        # get configs
        self.fps = config_manager.get_config('global', 'fps')

    def goto_scene(self, scene_name):
        self.next_scene = self.scenes[scene_name]

    def add_scene(self, scene_name, scene):
        self.scenes[scene_name] = scene

    def update(self):
        self.current_scene = self.next_scene
        self.current_scene.update()

    def draw(self, screen: pygame.Surface):
        self.current_scene.draw(screen)
