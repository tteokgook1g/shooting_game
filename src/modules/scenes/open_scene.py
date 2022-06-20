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

    def __init__(self, background: pygame.Surface, settings_image: pygame.Surface):
        super().__init__()
        self.settings_image = settings_image
        self.background = background
        self.state = -1
        self.center = (StateManager.get_state('global', 'screen_rect').center[0], StateManager.get_state(
            'global', 'screen_rect').center[1])

    def start_scene(self):
        # 음악을 불러와서 재생한다
        self.bgm = StateManager.get_state('global', 'opening_bgm')
        self.bgm.play(-1)

    def start_game(self):
        '''
        start_game event를 실행한다
        '''
        self.bgm.stop()  # 음악을 멈춘다
        self.call_event('start_game')

    def update(self):
        '''
        KEY_SPACE가 눌러져 있는지 확인한다
        '''
        if pygame.event.peek(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.state = self.state * -1
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.start_game()

    def draw(self, screen: pygame.Surface):
        '''
        start text를 화면에 blit한다
        '''

        blit_item(screen, self.background, topleft=(0, 0))
        if self.state == -1:
            blit_text(
                screen=screen,
                msg="Press SPACE to start the game",
                color=StateManager.get_state('global', 'text_color'),
                center=self.center
            )
            blit_text(
                screen=screen,
                msg="4.3을 향하여",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-200)
            )
            blit_text(
                screen=screen,
                msg="press ESCAPE to set settings",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-100)
            )
        # else:
        #     blit_text(
        #         screen=screen,
        #         msg="",
        #         color=StateManager.get_state('global', 'text_color'),
        #         center=(self.center[0], self.center[1]-100)
        #     )
        #     blit_text(
        #         screen=screen,
        #         msg="press ESCAPE to set settings",
        #         color=StateManager.get_state('global', 'text_color'),
        #         center=(self.center[0], self.center[1]-100)
        #     )
        #     blit_text(
        #         screen=screen,
        #         msg="press ESCAPE to set settings",
        #         color=StateManager.get_state('global', 'text_color'),
        #         center=(self.center[0], self.center[1]-100)
        #     )
