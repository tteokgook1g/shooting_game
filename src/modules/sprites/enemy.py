# 5.3 class Enemy


from ...interfaces.entity import Entity
from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager


class Enemy(Entity):
    def __init__(self, **kwargs):
        '''
        pos: (x, y) | 초기 위치
        img: pygame.Surface | 이미지
        speed: (speed_x, speed_y) | 초기 속도
        boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제

        score: int | 적이 죽으면 받는 점수
        health: int | 체력
        power: int | 공격력, 플레이어와 충돌 시 플레이어가 받는 피해량
        typeid: str | 적의 종류를 저장한다
        '''
        super().__init__(**kwargs)
        self.health = kwargs['health']
        self.score = kwargs['score']
        self.power = kwargs['power']
        self.typeid = kwargs['typeid']
        self.entity_manager = EntityManagerFactory.get_manager('enemy')
        self.entity = self

    def do_when_collide_with_player(self, player):
        '''
        자신을 삭제하고 플레이어의 체력을 차감한다
        '''
        self.destroy()
        player.add_health(-self.power)

    def destroy(self):
        super().destroy()
        StateManager.add_score(self.score)

    def attacked(self, attack_power: int):
        '''
        적은 attack_power만큼 피해를 입는다
        '''
        self.health -= attack_power
        # 체력이 0이하이면 죽는다
        if self.health <= 0:
            self.destroy()
