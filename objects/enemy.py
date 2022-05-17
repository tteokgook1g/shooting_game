# 5.3 class Enemy

import pygame
from .entity import Entity
from .player import Player


class Enemy(Entity):
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], func_delete, boundary_rect: pygame.Rect, score: int, health=100):
        super().__init__(pos, img, speed, func_delete, boundary_rect)
        self.health = health
        self.score = score

    def do_when_collide_with_player(self, player: Player):
        self.delete(self)

    def attacked(self, power: int):
        '''
        it returns score for attack
        enemy is attacked by power
        '''
        self.health -= power
        # delete when health <= 0
        if self.health <= 0:
            self.delete(self)
            return self.score
        return 0
