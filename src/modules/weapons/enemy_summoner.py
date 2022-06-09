'적을 소환하는 클래스를 정의한다'

import random

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ...interfaces.timer import ManualTimer, TimerManager
from ..sprites.enemy import Enemy


class EnemySummoner():
    'interface ItemSummoner'

    def __init__(self):
        self.enemies = EntityManagerFactory.get_manager('enemy')

    def summon(self):
        pass


class EnemySummonerDecorator(EnemySummoner):
    'interface WeaponDecorator'

    def __init__(self, summoner: EnemySummoner) -> None:
        super().__init__()
        self._summoner = summoner

    def summon(self):
        self._summoner.summon()


class DefaultStage1EnemySummoner(EnemySummoner):
    '체력을 채워주는 아이템 소환'

    def __init__(self, cooltime_range: tuple[int, int]):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_stage1_enemy_summoner')

        self.cooltime_range = cooltime_range

    def summon(self):
        '''
        새로운 적을 생성한다
        '''

        if self.timer.time <= 0:
            self.make_enemy()
            self.timer.time = random.randint(*self.cooltime_range)

    def make_enemy(self):
        '''
        새로운 적을 생성한다
        self.ENEMY_IMAGES 중 랜덤 이미지를 사용한다
        '''
        # get config
        offset = StateManager.get_config('enemy', 'enemy_offset_width')
        screen_width = StateManager.get_config('global', 'screen_width')
        enemy_imgs = StateManager.get_config('enemy', 'imgs')
        enemyid = random.randint(0, len(enemy_imgs)-1)

        new_enemy = Enemy(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=enemy_imgs[enemyid],
            speed=(0, StateManager.get_config('enemy', 'speed')),
            boundary_rect=StateManager.get_config(
                'stage1', 'entity_boundary'),
            score=StateManager.get_config('enemy', 'score'),
            health=StateManager.get_config('enemy', 'health'),
            power=StateManager.get_config('enemy', 'power'),
            typeid=f'default{enemyid}'
        )

        self.enemies.add_entity(new_enemy)

    def delete_enemy(self, enemy):
        self.enemies.remove_entity(enemy)

    def add_score(self, adding_score: int):
        StateManager.set_config(
            'global',
            'score',
            StateManager.get_config('global', 'score')+adding_score
        )
