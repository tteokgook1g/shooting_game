# 5.2 non-player interface

import pygame


class Entity():

    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], func_delete, boundary_rect: pygame.Rect):
        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.delete = func_delete
        self.boundary_rect = boundary_rect

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        # delete if self is out of screen
        if not self.get_rect().colliderect(self.boundary_rect):
            self.delete(self)

    def get_rect(self):
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)
