# 5.1 class Player

import pygame


class Player():
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], boundary_rect: pygame.Rect, power: int):
        '''
        pos: (x, y) | initial position
        img: pygame.Surface | image
        speed: (speed_x, speed_y) | initial speed
        boundary_rect: pygame.Rect | boundary
        power: int | attack power
        '''

        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.boundary_rect = boundary_rect
        self.power = power

    def moveto(self, x, y):
        self.pos = [x, y]
        self.check_boundary()

    def move(self, keys):
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
        rect = self.img.get_rect()
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)
