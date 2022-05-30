'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ..render_items import *


class open_scene(Scene):
    def __init__(self, config_manager: ConfigManager, background: pygame.Surface):
        super().__init__(config_manager)
        self.background = background
    def start_game(self):
        self.call_event("start_game")
        
    def update(self):
        pass
    # def draw(self, screen: pygame.Surface):
    #     blit_item(screen, self.background, topleft=(0, 0))
    #     draw_text(
    #         screen=screen,
    #         msg=f'Score: {str(self.score).zfill(6)}',
    #         color=self.configs.get_config('global', 'text_color'),
    #         center=self.configs.get_config('global', 'screen_rect').center

        