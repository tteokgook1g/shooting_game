'''
class Boss1
'''

import pygame
import random
import numpy
from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ..weapons.boss_weapon import BossWeapon
from .enemy import Enemy
from .player import Player


class Boss1(Enemy):
    '''
    죽을 때 EventListener.call_event('delete') 호출
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
        typeid: str | 적의 종류를 저장한다
        '''
        super().__init__(**kwargs)

        self.entity_manager = EntityManagerFactory.get_manager('enemy')
        self.entity = self
        self.max_health = self.health
        self.weapon = None
        self.counter=10
        self.direction=1

    def set_weapon(self, weapon: BossWeapon):
        self.weapon = weapon

    def attack(self):
        self.weapon.attack()

    def do_when_collide_with_player(self, player: Player):
        '''
        플레이어의 체력을 차감한다
        '''
        player.add_health(-self.power)

    def update(self):
        k = 2.5
        cx = self.get_rect().centerx
        screenx = StateManager.get_state('stage1', 'entity_boundary').centerx
        if cx<=49:
            self.speed[0]=2.5
        if cx>=400:
            self.speed[0]=-2.5
        if self.counter==0:
            self.speed[0]=k*(numpy.random.normal()+1)*self.direction
            self.direction*=-1
            self.counter=numpy.random.randint(10,20)
        self.counter-=1
        

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        # 체력 바
        bar_width, bar_height = 50, 7
        bar = pygame.Surface((bar_width, bar_height))
        bar.fill((255, 0, 0))
        pygame.draw.rect(bar, (0, 255, 0), [
                         0, 0, bar_width * self.health // self.max_health, bar_height])

        bar_rect = bar.get_rect()
        boss_rect = self.get_rect()
        bar_rect.center = boss_rect.centerx, boss_rect.bottom+10
        screen.blit(bar, bar_rect)

    def destroy(self):
        super().destroy()
        self.call_event('delete')
