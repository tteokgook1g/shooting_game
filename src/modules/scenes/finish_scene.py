'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ..render_items import *


class FinishScene(Scene):
    def __init__(self, config_manager: ConfigManager, score: int, background: pygame.Surface):
        super().__init__(config_manager)
        self.score = score
        self.background = background

    def update(self):
        self.score = self.configs.get_config('global', 'score')

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        draw_text(
            screen=screen,
            msg=f'Score: {str(self.score).zfill(6)}',
            color=self.configs.get_config('global', 'text_color'),
            center=self.configs.get_config('global', 'screen_rect').center
        )
