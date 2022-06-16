'보스의 공격을 정의한다'

import random

import pygame
from pygame import Vector2

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ...interfaces.timer import ManualTimer, TimerManager
from ..sprites.enemy import Enemy


class BossWeapon():
    'interface BossWeapon'

    def __init__(self):
        self.enemies = EntityManagerFactory.get_manager('enemy')
        self.boss = None

    def attack(self):
        pass

    def bind_boss(self, boss):
        '''
        self.boss을 입력받은 boss로 정한다
        '''
        self.boss = boss


class BossWeaponDecorator(BossWeapon):
    'interface WeaponDecorator'

    def __init__(self, weapon: BossWeapon) -> None:
        super().__init__()
        self._weapon = weapon

    def attack(self):
        self._weapon.attack()

    def bind_boss(self, boss):
        '''
        bossweapon을 가질 boss를 정한다
        '''
        super().bind_boss(boss)
        self._weapon.bind_boss(boss)


class DefaultStage1BossWeapon(BossWeapon):
    def __init__(self, cooltime_range: tuple[int, int]):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_stage1_boss_weapon')

        self.cooltime_range = cooltime_range

    def attack(self):
        '새로운 마법을 생성한다'
        if self.timer.time <= 0:
            self.make_spell()
            self.timer.time = random.randint(*self.cooltime_range)

    def make_spell(self):
        boss_rect = self.boss.get_rect()
        img: pygame.Surface = StateManager.get_state('boss1', 'spell_img')
        img_rect = img.get_rect()
        img_rect.centerx = boss_rect.centerx
        img_rect.top = boss_rect.bottom
        # new_spell(class Enemy) 생성
        new_spell = Enemy(
            pos=img_rect.topleft,
            img=img,
            speed=(0, StateManager.get_state('boss1', 'spell_speed')),
            boundary_rect=StateManager.get_state(
                'stage1', 'entity_boundary'),
            score=0,
            health=1000000,
            power=StateManager.get_state('boss1', 'spell_power'),
            typeid='boss1_spell1'
        )

        new_spell.add_event_listener(
            'delete', self.delete_enemy, new_spell)
        new_spell.add_event_listener(
            'add_score', lambda x: x, 0)  # blank function
        self.enemies.add_entity(new_spell)

    def delete_enemy(self, enemy):
        '''
        enemy entitiy를 제거한다
        '''
        self.enemies.remove_entity(enemy)


class DefaultStage2BossWeapon(BossWeapon):
    def __init__(self, cooltime_range: tuple[int, int]):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_stage2_boss_weapon')

        self.cooltime_range = cooltime_range

    def attack(self):
        '새로운 마법을 생성한다'
        if self.timer.time <= 0:
            self.make_enemy()
            self.timer.time = random.randint(*self.cooltime_range)

    def make_enemy(self):
        '''
        새로운 적을 생성한다
        self.ENEMY_IMAGES 중 랜덤 이미지를 사용한다
        '''
        # get config
        enemy_imgs = StateManager.get_state('enemy', 'imgs')
        enemyid = random.randint(0, len(enemy_imgs)-1)

        delta_pos = Vector2((150, 0)).rotate(random.random()*360)
        boss_pos = Vector2(self.boss.get_rect().center)
        # new_enemy(class Enemy) 생성
        new_enemy = Enemy(
            pos=(boss_pos+delta_pos)[:],
            img=enemy_imgs[enemyid],
            speed=(0, StateManager.get_state('enemy', 'speed')),
            boundary_rect=StateManager.get_state(
                'stage2', 'entity_boundary'),
            score=StateManager.get_state('enemy', 'score'),
            health=StateManager.get_state('enemy', 'health'),
            power=StateManager.get_state('enemy', 'power'),
            typeid=f'default{enemyid}'
        )

        self.enemies.add_entity(new_enemy)

    def delete_enemy(self, enemy):
        '''
        enemy entitiy를 제거한다
        '''
        self.enemies.remove_entity(enemy)

    def add_score(self, adding_score: int):
        '''
        호출되었을 때 adding_score만큼 score를 추가한다'''
        StateManager.set_state(
            'global',
            'score',
            StateManager.get_state('global', 'score')+adding_score
        )
