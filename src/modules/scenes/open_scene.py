'''
class FinishScene
'''

import pygame

from ...interfaces.game_state import StateManager

from ...interfaces.scene import Scene
from ...interfaces.utils import *


class OpeningScene(Scene):
    '''
    키보드를 누르면 EventListener.call_event('start_game')
    '''

    def __init__(self, background: pygame.Surface):
        super().__init__()
        self.background = background

    def start_game(self):
        '''
        start_game event를 실행한다
        '''
        self.call_event('start_game')

    def update(self):
        '''
        KEY_SPACE가 눌러져 있는지 확인한다
        '''
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.start_game()

    def draw(self, screen: pygame.Surface):
        '''
        start text를 화면에 blit한다
        '''
        blit_item(screen, self.background, topleft=(0, 0))
        blit_text(
            screen=screen,
            msg="Press SPACE to start the game",
            color=StateManager.get_state('global', 'text_color'),
            center=StateManager.get_state('global', 'screen_rect').center
        )
