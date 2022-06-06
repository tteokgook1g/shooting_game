'''
다양한 무기 클래스를 정의한다.
'''

from typing import Callable

import pygame
from ...interfaces.entity_manager import EntityManagerFactory
from pygame import Vector2

from ...interfaces.object_configs import ConfigManager
from ...interfaces.timer import ManualTimer, TimerManager
from ..sprites.bullet import Bullet


class PlayerWeapon():
    'interface weapon'

    def __init__(self):
        self.player = None
        self.bullets = EntityManagerFactory.get_manager('bullet')

    def attack(self):
        pass

    def bind_player(self, player):
        self.player = player


class WeaponDecorator(PlayerWeapon):
    'interface WeaponDecorator'

    def __init__(self, weapon: PlayerWeapon) -> None:
        super().__init__()
        self._weapon = weapon

    def attack(self):
        self._weapon.attack()

    def bind_player(self, player):
        super().bind_player(player)
        self._weapon.bind_player(player)


class DefaultPlayerWeapon(PlayerWeapon):
    '''
    spacebar로 쿨타임마다 공격한다.
    '''

    def __init__(self, cooltime: int):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_player_weapon')

        self.cooltime = cooltime

    def attack(self):
        '''
        새로운 총알을 생성한다
        '''
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.make_bullet()
            self.timer.time = self.cooltime

    def make_bullet(self):
        '''
        callback of weapon
        새로운 총알을 생성한다
        '''

        # get config
        bullet_img: pygame.Surface = ConfigManager.get_config(
            'bullet', 'bullet_img')

        player_rect: pygame.Rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = bullet_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        new_bullet = Bullet(
            pos=img_rect.topleft,
            img=bullet_img,
            speed=(0, -ConfigManager.get_config('bullet', 'speed')),
            boundary_rect=ConfigManager.get_config(
                'stage2', 'entity_boundary'),
            power=self.player.power
        )
        new_bullet.add_event_listener(
            'delete', self.delete_bullet, new_bullet)
        self.bullets.add_entity(new_bullet)

    def delete_bullet(self, bullet):
        self.bullets.remove_entity(bullet)


class ShotgunDecorator(WeaponDecorator):
    def __init__(self, weapon: PlayerWeapon, cooltime: int):
        super().__init__(weapon)

        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'player_shotgun')

        self.cooltime = cooltime

    def attack(self):
        super().attack()
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_e]:
            self.make_shotgun()
            self.timer.time = self.cooltime

    def make_shotgun(self):
        '''
        callback of weapon
        새로운 총알 여러 개를 생성한다
        '''
        NUM_OF_BULLET = 24

        # get config
        shotgun_img: pygame.Surface = ConfigManager.get_config(
            'bullet', 'shotgun_img')

        player_rect: pygame.Rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = shotgun_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        speed = ConfigManager.get_config('bullet', 'speed')
        boundary_rect = ConfigManager.get_config(
            'stage2', 'entity_boundary')

        for i in range(NUM_OF_BULLET):
            delta_pos = Vector2((5, 0))
            delta_pos.rotate_ip(360*i/NUM_OF_BULLET)
            new_pos = (Vector2(player_rect.center)+delta_pos)[:]
            new_rect = img_rect.copy()
            new_rect.center = new_pos

            new_bullet = Bullet(
                pos=new_rect.topleft,
                img=shotgun_img,
                speed=(speed*delta_pos.normalize())[:],
                boundary_rect=boundary_rect,
                power=self.player.power//4
            )
            new_bullet.add_event_listener(
                'delete', self.delete_bullet, new_bullet)
            self.bullets.add_entity(new_bullet)

    def delete_bullet(self, bullet):
        self.bullets.remove_entity(bullet)
