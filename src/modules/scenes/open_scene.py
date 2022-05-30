'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ..render_items import *


class OpeningScene(Scene):
    '''
    키보드를 누르면 EventListener.call_event('start_game')
    '''

    def __init__(self, config_manager: ConfigManager, background: pygame.Surface):
        super().__init__(config_manager)
        self.background = background

    def start_game(self):
        self.call_event('start_game')

    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.start_game()

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
