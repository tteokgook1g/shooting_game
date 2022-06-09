'''
interface Entity
'''


import pygame
from pygame import Vector2

from .event_listener import EventListener


class Entity(EventListener):
    def __init__(self, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
        '''
        super().__init__()

        self.pos: Vector2 = Vector2(kwargs['pos'][:])
        self.img: pygame.Surface = kwargs['img']
        self.speed: Vector2 = Vector2(kwargs['speed'][:])
        self.boundary_rect: pygame.Rect = kwargs['boundary_rect']
        self.entity_manager = None  # 이 엔티티가 포함된 엔티티매니저 참조
        self.entity = None  # 이 엔티티를 참조

    def move(self):
        '''
        self.speed만큼 이동한다
        '''
        self.pos += self.speed
        # destroy if self is out of screen
        if not self.get_rect().colliderect(self.boundary_rect):
            self.destroy()

    def get_rect(self):
        '''
        이것의 rect를 return한다
        '''
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def get_pos(self) -> tuple[int, int]:
        return self.pos[:]

    def draw(self, screen: pygame.Surface):
        '''
        screen에 blit한다
        '''
        screen.blit(self.img, self.pos[:])

    def destroy(self):
        self.entity_manager.remove_entity(self.entity)
