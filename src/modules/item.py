'''
class Item
'''

from .entity import Entity
from .player import Player


class Item(Entity):
    '''
    플레이어와 닿을 때 EventListener.call_event('delete')
    '''

    def __init__(self, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제

        heal: int | 플레이어가 얻는 체력
        '''
        super().__init__(**kwargs)
        self.heal = kwargs['heal']

    def do_when_collide_with_player(self, player: Player):
        '''
        자신을 삭제하고 플레이어의 체력을 차감한다
        '''
        self.call_event('delete')
        player.add_health(self.heal)
