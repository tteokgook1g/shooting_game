'''
class FinishScene
'''

import pygame

from src.interfaces.scene import Scene
from src.interfaces.object_configs import *
from ..render_items import *


class OpeningScene(Scene):
    '''
    키보드를 누르면 EventListener.call_event('start_game')
    '''

    def __init__(self, config_manager: ConfigManager, background: pygame.Surface, font:pygame.font):
        super().__init__(config_manager)
        self.background = background
        self.font= font

    def start_game(self):
        self.call_event('start_game')

    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.start_game()

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        text= self.font.render("4.3을 위하여",True, (0,0,0))
        screen.blit(text,(100,120))
        draw_text(
            screen=screen,
            msg="Press SPACE to start the game",
            color=self.configs.get_config('global', 'text_color'),
            center=self.configs.get_config('global', 'screen_rect').center
        )
        
