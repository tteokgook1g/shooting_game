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
        center = StateManager.get_state('global', 'screen_rect').center
        blit_text(
            screen=screen,
            msg=f'Score: {str(StateManager.get_score()).zfill(6)}',
            color=StateManager.get_state('global', 'text_color'),
            center=center
        )
        blit_text(
            screen=screen,
            msg=f"학점: {str(StateManager.get_state('player', 'grade'))}",
            color=StateManager.get_state('global', 'text_color'),
            center=(center[0], center[1]+50)
        )
