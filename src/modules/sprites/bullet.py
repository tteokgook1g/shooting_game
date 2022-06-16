# class Bullet


from ...interfaces.entity import Entity
from ...interfaces.entity_manager import EntityManagerFactory
from .enemy import Enemy


class Bullet(Entity):
    '''
    죽을 때 EventListener.call_event('delete') 호출
    '''

    def __init__(self, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제

        power: int | 공격력
        '''

        super().__init__(**kwargs)
        self.entity_manager = EntityManagerFactory.get_manager('bullet')
        self.entity = self
        self.power = kwargs['power']

    def do_when_collide_with_enemy(self, enemy: Enemy):
        '''
        적에게 self.power만큼 피해를 입힌다
        적이 죽으면 func_increase_score(score)을 실행한다
        '''
        self.destroy()
        enemy.attacked(self.power)
