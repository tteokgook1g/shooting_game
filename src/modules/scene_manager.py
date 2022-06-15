'''
class SceneManager
'''

import pygame

from ..interfaces.event_listener import EventListener
from ..interfaces.game_state import StateManager
from ..interfaces.scene import Scene


class SceneManager(EventListener):
    def __init__(self):
        super().__init__()
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene = None
        self.next_scene: Scene = None
        self.fps = StateManager.get_state('global', 'fps')

    def goto_scene(self, scene_name):
        self.next_scene = self.scenes[scene_name]

    def add_scene(self, scene_name, scene):
        self.scenes[scene_name] = scene

    def update(self):
        # get configs
        self.fps = StateManager.get_state('global', 'fps')
        if self.current_scene != self.next_scene:
            self.current_scene = self.next_scene
            self.current_scene.start_scene()
        self.current_scene.update()

    def draw(self, screen: pygame.Surface):
        self.current_scene.draw(screen)
