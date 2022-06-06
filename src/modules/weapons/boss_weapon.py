'보스의 공격을 정의한다'

import pygame
import random
from pygame import Vector2

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.object_configs import ConfigManager
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
        self.boss = boss


class BossWeaponDecorator(BossWeapon):
    'interface WeaponDecorator'

    def __init__(self, weapon: BossWeapon) -> None:
        super().__init__()
        self._weapon = weapon

    def attack(self):
        self._weapon.attack()

    def bind_boss(self, boss):
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
        img: pygame.Surface = ConfigManager.get_config('boss1', 'spell_img')
        img_rect = img.get_rect()
        img_rect.centerx = boss_rect.centerx
        img_rect.top = boss_rect.bottom
        new_spell = Enemy(
            pos=img_rect.topleft,
            img=img,
            speed=(0, ConfigManager.get_config('boss1', 'spell_speed')),
            boundary_rect=ConfigManager.get_config(
                'stage1', 'entity_boundary'),
            score=0,
            health=1000000,
            power=ConfigManager.get_config('boss1', 'spell_power'),
            typeid='boss1_spell1'
        )

        new_spell.add_event_listener(
            'delete', self.delete_enemy, new_spell)
        new_spell.add_event_listener(
            'add_score', lambda x: x, 0)  # blank function
        self.enemies.add_entity(new_spell)

    def delete_enemy(self, enemy):
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
        enemy_imgs = ConfigManager.get_config('enemy', 'imgs')
        enemyid = random.randint(0, len(enemy_imgs)-1)

        delta_pos = Vector2((150, 0)).rotate(random.random()*360)
        boss_pos = Vector2(self.boss.get_rect().center)

        new_enemy = Enemy(
            pos=(boss_pos+delta_pos)[:],
            img=enemy_imgs[enemyid],
            speed=(0, ConfigManager.get_config('enemy', 'speed')),
            boundary_rect=ConfigManager.get_config(
                'stage2', 'entity_boundary'),
            score=ConfigManager.get_config('enemy', 'score'),
            health=ConfigManager.get_config('enemy', 'health'),
            power=ConfigManager.get_config('enemy', 'power'),
            typeid=f'default{enemyid}'
        )
        new_enemy.add_event_listener('delete', self.delete_enemy, new_enemy)
        new_enemy.add_event_listener(
            'add_score', self.add_score, new_enemy.score)
        self.enemies.add_entity(new_enemy)

    def delete_enemy(self, enemy):
        self.enemies.remove_entity(enemy)

    def add_score(self, adding_score: int):
        ConfigManager.set_config(
            'global',
            'score',
            ConfigManager.get_config('global', 'score')+adding_score
        )
