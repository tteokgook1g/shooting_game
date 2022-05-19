'''
모든 object의 config interface를 정의한다
'''

import pygame
from typing import Callable


class PlayerConfig():
    def __init__(
            self,
            pos: tuple[int, int],
            img: pygame.Surface,
            speed: tuple[int, int],
            boundary_rect: pygame.Rect,
            power: int,
            health: int):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계
        power: int | 공격력
        health: int | 체력
        '''

        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.boundary_rect = boundary_rect
        self.power = power
        self.health = health


class EntityConfig():
    def __init__(
            self,
            pos: tuple[int, int],
            img: pygame.Surface,
            speed: tuple[int, int],
            boundary_rect: pygame.Rect):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
        '''

        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.boundary_rect = boundary_rect
