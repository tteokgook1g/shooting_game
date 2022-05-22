# 5.4 class Bullet

from typing import Callable
import pygame

from ..interfaces.object_configs import EntityConfig
from .entity import Entity
from .enemy import Enemy


class Bullet(Entity):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(
            self,
            entity_config: EntityConfig,
            power: int):
        '''
        power: int | 공격력

        -EntityConfig
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
        '''

        super().__init__(entity_config)
        self.power = power  # attack power

    def do_when_collide_with_enemy(self, enemy: Enemy, func_increase_score: Callable[[int], None] = None):
        '''
        적에게 self.power만큼 피해를 입힌다
        적이 죽으면 func_increase_score(score)을 실행한다
        '''
        self.call_event('delete')
        enemy.attacked(self.power, func_increase_score)