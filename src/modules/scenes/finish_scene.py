'''
class FinishScene
'''

import pygame

from ...interfaces.game_state import *
from ...interfaces.scene import Scene
from ...interfaces.utils import *


class FinishScene(Scene):
    def __init__(self, score: int, background: pygame.Surface):
        super().__init__()
        self.score = score
        self.background = background

    def update(self):
        self.score = StateManager.get_score()

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        blit_text(
            screen=screen,
            msg=f'Score: {str(self.score).zfill(6)}',
            color=StateManager.get_state('global', 'text_color'),
            center=StateManager.get_state('global', 'screen_rect').center
        )
