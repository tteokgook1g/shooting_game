'''
class Player
'''

import pygame
from pygame import Vector2

from ...interfaces.event_listener import EventListener
from ...interfaces.game_state import StateManager
from ..weapons.player_weapon import PlayerWeapon
from ...interfaces.utils import *


class Player(EventListener):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(self):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어날 수 없음
        weapon: PlayerWeapon | 플레이어의 무기
        power: int | 공격력
        health: int | 체력
        '''

        super().__init__()
        default_speed = StateManager.get_state('player', 'speed')

        StateManager.get_state('player', 'pos')
        self.pos: Vector2 = Vector2(StateManager.get_state('player', 'pos'))
        self.img: pygame.Surface = StateManager.get_state('player', 'img')
        self.speed: Vector2 = Vector2((default_speed, default_speed))
        self.boundary_rect: pygame.Rect = StateManager.get_state(
            'player', 'boundary_rect')
        self.weapon: PlayerWeapon = StateManager.get_state(
            'player', 'weapon')
        self.power = StateManager.get_state('player', 'power')
        self.health: int = StateManager.get_state('player', 'health')
        self.max_health = self.health

    def get_pos(self) -> tuple[int, int]:
        return self.pos[:]

    def add_health(self, health):
        '''
        체력을 health만큼 더한다
        음수도 가능하다
        '''
        self.health += health
        if self.health <= 0:
            self.call_event('delete')

    def render_health_bar(self):
        bar_width, bar_height = 16, 100
        bar = pygame.Surface((bar_width, bar_height+20))
        bar.fill((255, 255, 255))
        pygame.draw.rect(bar, (255, 0, 0), [
                         0, 0, bar_width, bar_height])
        pygame.draw.rect(bar, (0, 255, 0), [
                         0, 0, bar_width, bar_height * self.health // self.max_health])
        heart = pygame.image.load('./asset/img/heart.png')
        blit_item(bar, heart, bottomright=bar.get_rect().bottomright)

        return bar

    def moveto(self, x, y):
        '''
        (x, y)로 움직인다
        '''
        self.pos[:] = [x, y]
        self.check_boundary()

    def move(self, keys):
        '''
        wasd로 움직인다
        '''
        prev = self.pos[:]
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed[0]
        if keys[pygame.K_d]:
            self.pos[0] += self.speed[0]
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed[1]
        if keys[pygame.K_s]:
            self.pos[1] += self.speed[1]

        if prev != self.pos:
            self.check_boundary()

    def check_boundary(self):
        '''
        경계 밖으로 벗어나면 경계 안으로 옮긴다
        '''
        player_rect = self.get_rect()
        left = self.boundary_rect.left
        right = self.boundary_rect.right - player_rect.width
        top = self.boundary_rect.top
        bottom = self.boundary_rect.bottom - player_rect.height

        if self.pos[0] < left:
            self.pos[0] = left
        elif self.pos[0] > right:
            self.pos[0] = right
        if self.pos[1] < top:
            self.pos[1] = top
        elif self.pos[1] > bottom:
            self.pos[1] = bottom

    def get_rect(self):
        '''
        이것의 rect를 return한다
        '''
        rect = self.img.get_rect()
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def set_weapon(self, weapon: PlayerWeapon):
        self.weapon = weapon

    def attack(self):
        self.weapon.attack()

    def draw(self, screen: pygame.Surface):
        '''
        screen에 blit한다
        '''
        screen.blit(self.img, self.pos[:])
