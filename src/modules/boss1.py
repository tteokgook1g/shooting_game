'''
class Boss1
'''
import pygame

from .enemy import Enemy
from .entity import Entity
from ..interfaces.object_configs import ConfigManager


class Boss1(Enemy):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(self, config_manager: ConfigManager, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제

        score: int | 적이 죽으면 받는 점수
        health: int | 체력
        power: int | 공격력, 플레이어와 충돌 시 플레이어가 받는 피해량
        '''
        super().__init__(**kwargs)
        self.configs = config_manager

    def summon_spell(self):
        '''
        spell을 생성하여 return한다
        '''
        boss_rect = self.get_rect()
        img: pygame.Surface = self.configs.get_config('boss1', 'spell_img')
        img_rect = img.get_rect()
        img_rect.centerx = boss_rect.centerx
        img_rect.top = boss_rect.bottom
        return Enemy(
            pos=img_rect.topleft,
            img=img,
            speed=self.configs.get_config('boss1', 'spell_speed'),
            boundary_rect=self.configs.get_config('enemy', 'boundary_rect'),
            score=0,
            health=1000000,
            power=self.configs.get_config('boss1', 'spell_power')
        )

    def update(self):
        k = 1/10
        cx = self.get_rect().centerx
        vx = self.speed[0]
        screenx = self.configs.get_config(
            'global', 'screen_rect').centerx
        self.speed = (vx+k*(screenx-cx), 0)
