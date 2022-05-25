'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ..render_items import *


class StartScene(Scene):
    '''
    키보드를 누르면 EventListener.call_event('start_game')
    '''

    def __init__(self, config_manager: ConfigManager, background: pygame.Surface):
        super().__init__(config_manager)
        self.background = background

    def update(self):
        for key in pygame.key.get_pressed():
            if key:
                self.call_event('start_game')

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        draw_text(
            screen=screen,
            msg='press any key to start',
            color=self.configs.get_config('global', 'text_color'),
            center=self.configs.get_config('global', 'screen_rect').center
        )
