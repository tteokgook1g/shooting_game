'''
다양한 무기 클래스를 정의한다.
'''

from typing import Callable
import pygame
from ..interfaces.timer import ManualTimer, TimerManager
from ..interfaces.object_configs import ConfigManager


class PlayerWeapon():
    'interface weapon'

    def __init__(self):
        self.player = None
        self.configs = None

    def attack(self):
        pass

    def bind_player(self, player):
        self.player = player

    def bind_config(self, config_manager: ConfigManager):
        self.configs = config_manager


class DefaultWeapon(PlayerWeapon):
    '''
    spacebar로 쿨타임마다 공격한다.
    '''

    def __init__(self, cooltime: int, make_bullet: Callable):
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'player_default_weapon')

        self.make_bullet = make_bullet
        self.cooltime = cooltime

    def attack(self):
        '''
        새로운 총알을 생성한다
        '''
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.make_bullet()
            self.timer.time = self.cooltime


class WeaponDecorator(PlayerWeapon):
    _weapon: PlayerWeapon = None

    def __init__(self, weapon: PlayerWeapon) -> None:
        self._weapon = weapon

    def attack(self):
        self._weapon.attack()


class ShotgunDecorator(WeaponDecorator):
    def __init__(self, weapon: PlayerWeapon, cooltime: int, make_shotgun: Callable):
        super().__init__(weapon)

        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'player_shotgun')

        self.make_shotgun = make_shotgun
        self.cooltime = cooltime

    def attack(self):
        super().attack()
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_e]:
            self.make_shotgun()
            self.timer.time = self.cooltime
