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

    def start_scene(self):
        # 음악을 불러와서 재생한다
        self.bgm = StateManager.get_state('global', 'opening_bgm')
        self.bgm.play(-1)

    def update(self):
        '''
        score변수를 player의 score로 변환한다
        '''
        self.score = StateManager.get_score()

    def draw(self, screen: pygame.Surface):
        '''
        game_over 화면에 score와 학점을 그린다
        '''
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
        if str(StateManager.get_state('player', 'grade'))[0] == 'C' or str(StateManager.get_state('player', 'grade'))[0] == 'D' or str(StateManager.get_state('player', 'grade'))[0] == 'F':
            blit_text(
                screen=screen,
                msg=f"조금 더 분발하세요...",
                color=StateManager.get_state('global', 'text_color'),
                center=(center[0], center[1]-50)
            )
        else:
            blit_text(
                screen=screen,
                msg=f"훌륭해요!",
                color=StateManager.get_state('global', 'text_color'),
                center=(center[0], center[1]-50)
            )
