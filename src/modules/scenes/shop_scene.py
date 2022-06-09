'''
class FinishScene
'''

import pygame

from ...interfaces.scene import Scene
from ...interfaces.utils import *
from ...interfaces.button import *


class ShopScene(Scene):
    '상점 장면'

    def __init__(self, background: pygame.Surface):
        def log():
            print('clicked')

        super().__init__()
        self.background = background
        self.buttons = ButtonManager()
        button = Button(pygame.Rect(0, 0, 100, 30))
        button.add_event_listener('click', log)
        self.buttons.add_button(button)

    def update(self):
        self.buttons.update()

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        self.buttons.draw(screen)
