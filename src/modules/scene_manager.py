# class SceneManager

import pygame

from ..interfaces.event_listener import EventListener
from ..interfaces.game_state import StateManager
from ..interfaces.scene import Scene


class SceneManager(EventListener):
    def __init__(self):
        '''
        scenes: dict[str,Scene] | Scene들을 Scene들의 이름과 함께 저장하는 dictionary
        current_scene: Scene | SceneManager를 update할 때 update되는 Scene
        next_scene: Scene | current_scene 이 끝났을 때 이동하게 되는 Scene
        fps: int | pygame의 fps
        '''
        super().__init__()
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene = None
        self.next_scene: Scene = None
        self.fps = StateManager.get_state('global', 'fps')

    def goto_scene(self, scene_name):
        'current_scene이 끝났을 때 이동할 next_scene을 설정한다'
        self.next_scene = self.scenes[scene_name]

    def add_scene(self, scene_name, scene):
        'scenes에 새로운 Scene을 추가한다'
        self.scenes[scene_name] = scene

    def update(self):
        'current_scene을 update 한다'
        self.fps = StateManager.get_state('global', 'fps')
        if self.current_scene != self.next_scene:
            self.current_scene = self.next_scene
            self.current_scene.start_scene()
        if self.current_scene is not None:
            self.current_scene.update()

    def draw(self, screen: pygame.Surface):
        'current_scene을 화면에 띄운다'
        if self.current_scene is not None:
            self.current_scene.draw(screen)
