# 5.3 class Enemy

from typing import Callable
import pygame


from .entity import Entity
from .player import Player


class Enemy(Entity):
    '''
    죽을 때
    EventListener.call_event('delete')
    EventListener.call_event('add_score')
    호출
    '''

    def __init__(self, **kwargs):
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
        self.health = kwargs['health']
        self.score = kwargs['score']
        self.power = kwargs['power']

    def do_when_collide_with_player(self, player: Player):
        '''
        자신을 삭제하고 플레이어의 체력을 차감한다
        '''
        self.delete()
        player.add_health(-self.power)

    def delete(self):
        self.call_event('add_score')
        self.call_event('delete')

    def attacked(self, attack_power: int, func_increase_score: Callable[[int], None] = None):
        '''
        적은 attack_power만큼 피해를 입는다
        적이 죽으면 func_increase_score(score)을 실행한다
        '''
        self.health -= attack_power
        # 체력이 0이하이면 죽는다
        if self.health <= 0:
            self.delete()
            # 점수를 증가시킨다
            func_increase_score(self.score)
        return 0
