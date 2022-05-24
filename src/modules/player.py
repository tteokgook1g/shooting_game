'''
class Player
'''

import pygame

from ..interfaces.event_listener import EventListener


class Player(EventListener):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(self, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어날 수 없음
        power: int | 공격력
        health: int | 체력
        '''

        super().__init__()

        self.pos: list[int, int] = list(kwargs['pos'])
        self.img: pygame.Surface = kwargs['img']
        self.speed: list[int, int] = list(kwargs['speed'][:])
        self.boundary_rect: pygame.Rect = kwargs['boundary_rect']
        self.power: int = kwargs['power']
        self.health: int = kwargs['health']

    def add_health(self, health):
        '''
        체력을 health만큼 더한다
        음수도 가능하다
        '''
        self.health += health
        if self.health <= 0:
            self.call_event('delete')

    def moveto(self, x, y):
        '''
        (x, y)로 움직인다
        '''
        self.pos = [x, y]
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

    def draw(self, screen: pygame.Surface):
        '''
        screen에 blit한다
        '''
        screen.blit(self.img, self.pos)
