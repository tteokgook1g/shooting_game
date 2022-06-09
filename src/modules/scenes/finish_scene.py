'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ...interfaces.utils import *


class FinishScene(Scene):
    def __init__(self, score: int, background: pygame.Surface):
        super().__init__()
        self.score = score
        self.background = background

    def update(self):
        self.score = ConfigManager.get_config('global', 'score')

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        draw_text(
            screen=screen,
            msg=f'Score: {str(self.score).zfill(6)}',
            color=ConfigManager.get_config('global', 'text_color'),
            center=ConfigManager.get_config('global', 'screen_rect').center
        )
