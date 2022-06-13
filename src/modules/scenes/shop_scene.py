'''
class FinishScene
'''

import pygame

from ...interfaces.scene import Scene
from ...interfaces.utils import *
from ...interfaces.button import *
from ..weapons.player_weapon import *


class ShopScene(Scene):
    '상점 장면'

    def __init__(self, background: pygame.Surface):
        def log():
            print('clicked')

        super().__init__()
        self.background = background

        default_weapon = DefaultPlayerWeapon(
            cooltime=10)
        button1 = Button(pygame.Rect(135, 400, 100, 30))
        button1.add_event_listener('click', default_weapon.purchase_level_up)
        ButtonManager.add_button(button1)

        player_weapon = ShotgunDecorator(default_weapon, 30)
        button2 = Button(pygame.Rect(245, 400, 100, 30))
        button2.add_event_listener('click', player_weapon.purchase_level_up)
        ButtonManager.add_button(button2)

        self.weapon = player_weapon

    def update(self):
        self.shop_info = self.weapon.render_shop_info()
        ButtonManager.update()

    def draw(self, screen: pygame.Surface):
        blit_item(screen, self.background, topleft=(0, 0))
        ButtonManager.draw(screen)
        blit_item(screen, self.shop_info, center=screen.get_rect().center)
        blit_text(screen, f'Gold : {int(StateManager.get_gold())}',
                  topright=screen.get_rect().topright)
