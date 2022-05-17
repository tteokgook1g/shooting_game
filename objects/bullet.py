# 5.4 class Bullet

import pygame
from .entity import Entity
from .enemy import Enemy


class Bullet(Entity):
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], boundary_rect: pygame.Rect, power: int, func_delete):
        super().__init__(pos, img, speed, func_delete, boundary_rect)
        self.power = power  # attack power

    def do_when_collide_with_enemy(self, enemy: Enemy):
        '''
        it returns score for attack
        '''
        self.delete(self)
        return enemy.attacked(self.power)
