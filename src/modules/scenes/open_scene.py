'''
class FinishScene
'''

from sre_parse import State
import pygame

from ...modules.scenes.game_stage import GameStage
from ...interfaces.game_state import StateManager

from ...interfaces.scene import Scene
from ...interfaces.utils import *


class OpeningScene(Scene):
    '''
    키보드를 누르면 EventListener.call_event('start_game')
    '''

    def __init__(self, background: pygame.Surface, settings_image: pygame.Surface):
        super().__init__()
        self.current_settings = {1: 'health', 2: 'boss1_health', 3: 'speed'}
        self.current_setting = 1
        self.settings_image = settings_image
        self.background = background
        self.state = -1
        self.center = (StateManager.get_state('global', 'screen_rect').center[0], StateManager.get_state(
            'global', 'screen_rect').center[1])

    def start_game(self):
        '''
        start_game event를 실행한다
        '''
        self.call_event('start_game')

    def update(self):
        '''
        KEY_SPACE가 눌러져 있는지 확인한다
        '''
        if pygame.event.peek(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.state = self.state * -1
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.current_setting += 1
                if self.current_setting > 3:
                    self.current_setting -= 3
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.current_setting -= 1
                if self.current_setting < 1:
                    self.current_setting += 3
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.start_game()
        if self.current_setting == 1:
            if pygame.key.get_pressed()[pygame.K_q]:
                StateManager.set_state(
                    'player', 'health', StateManager.get_state('player', 'health') - 5)
            if pygame.key.get_pressed()[pygame.K_e]:
                StateManager.set_state(
                    'player', 'health', StateManager.get_state('player', 'health') + 5)
        if self.current_setting == 2:
            if pygame.key.get_pressed()[pygame.K_q]:
                StateManager.set_state(
                    'boss1', 'boss1_health', StateManager.get_state('boss1', 'boss1_health') - 10)
            if pygame.key.get_pressed()[pygame.K_e]:
                StateManager.set_state(
                    'boss1', 'boss1_health', StateManager.get_state('boss1', 'boss1_health') + 10)
        if self.current_setting == 3:
            if pygame.key.get_pressed()[pygame.K_q]:
                StateManager.set_state(
                    'player', 'speed', StateManager.get_state('player', 'speed') - 0.1)
            if pygame.key.get_pressed()[pygame.K_e]:
                StateManager.set_state(
                    'player', 'speed', StateManager.get_state('player', 'speed') + 0.1)

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
                msg="4.3을 위하여",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-200)
            )
            blit_text(
                screen=screen,
                msg="press ESCAPE to set settings",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-100)
            )
        if self.state == 1:
            blit_text(
                screen=screen,
                msg=f"current setting is: {self.current_settings[self.current_setting]}",
                color=StateManager.get_state('global', 'text_color'),
                center=(200, 100)
            )
            # health
            blit_text(
                screen=screen,
                msg="set player health by Q and E",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-100)
            )
            blit_text(
                screen=screen,
                msg=f"{StateManager.get_state('player','health')}",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]-50)
            )
            # health_finish
            # boss1_health
            blit_text(
                screen=screen,
                msg="set boss1 health by Q and E",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1])
            )
            blit_text(
                screen=screen,
                msg=f"{StateManager.get_state('boss1', 'boss1_health')}",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]+50)
            )
            # boss1_health_finish
            # player_speed
            blit_text(
                screen=screen,
                msg="set player speed by Q and E",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]+100)
            )
            blit_text(
                screen=screen,
                msg=f"{StateManager.get_state('player','speed'):.2f}",
                color=StateManager.get_state('global', 'text_color'),
                center=(self.center[0], self.center[1]+150)
            )
            # player_finish
