'''
interface Entity
'''

from typing import Callable
import pygame

from ..interfaces.event_listener import EventListener
from ..interfaces.object_configs import EntityConfig


class Entity(EventListener):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(self, entity_config: EntityConfig):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
        '''
        super().__init__()

        self.pos = list(entity_config.pos[:])
        self.img = entity_config.img
        self.speed = list(entity_config.speed[:])
        self.boundary_rect = entity_config.boundary_rect

    def move(self):
        '''
        self.speed만큼 이동한다
        '''
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        # delete if self is out of screen
        if not self.get_rect().colliderect(self.boundary_rect):
            self.call_event('delete')

    def get_rect(self):
        '''
        이것의 rect를 return한다
        '''
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen: pygame.Surface):
        '''
        screen에 blit한다
        '''
        screen.blit(self.img, self.pos)
