'두 번째 스테이지'

import pygame

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ...interfaces.scene import Scene
from ...interfaces.timer import *
from ...interfaces.utils import *
from ..sprites.boss import Boss1
from ..sprites.player import Player
from ..weapons.boss_weapon import *
from ..weapons.enemy_summoner import *
from ..weapons.item_summoner import *
from ..weapons.player_weapon import *


class AroundStage(Scene):
    '''
    게임의 스테이지 하나
    스테이지를 시작학 때 start_scene 호출 필요
    게임이 끝날 때 EventListener.call_event('game_over')
    보스를 잡았을 때 EventListener.call_event('stage_clear')
    '''

    def __init__(
        self,
        level_interval: int,
    ):
        '''
        level_interval: int | 레벨의 점수 간격
        '''
        super().__init__()

        # 변수
        self.player = None
        self.boss: Boss1 = None
        self.enemies = None
        self.bullets = None
        self.items = None
        self.item_summoner = None
        self.level_interval = level_interval
        self.next_level_score = level_interval

    def start_scene(self):
        self.player = Player()
        self.enemies = EntityManagerFactory.get_manager('enemy')
        self.bullets = EntityManagerFactory.get_manager('bullet')
        self.items = EntityManagerFactory.get_manager('item')

        self.summon_boss()

        self.player.boundary_rect = StateManager.get_config(
            'stage2', 'entity_boundary')
        # 플레이어 무기
        default_weapon = DefaultPlayerWeapon(
            cooltime=10)
        player_weapon = ShotgunDecorator(default_weapon, 30)
        player_weapon.bind_player(self.player)
        self.player.set_weapon(player_weapon)

        # 소환자
        default_item_summoner = DefaultStage2ItemSummoner(
            cooltime_range=(25, 50),
            heal=StateManager.get_config('item', 'heal')
        )
        self.item_summoner = default_item_summoner

        # 타이머
        self.timer_manager = TimerManager()

        # add event_listener
        self.player.add_event_listener('delete', self.game_over)

    # callbacks ------------------------------------------------

    def summon_boss(self):
        img: pygame.Surface = StateManager.get_config('boss1', 'boss1_img')
        img_rect = img.get_rect()
        img_rect.top = 20
        img_rect.centerx = StateManager.get_config(
            'stage2', 'entity_boundary').centerx
        self.boss = Boss1(
            pos=img_rect.topleft,
            img=StateManager.get_config('boss1', 'boss1_img'),
            speed=(StateManager.get_config('boss1', 'boss1_speed'), 0),
            boundary_rect=StateManager.get_config(
                'stage2', 'entity_boundary'),
            score=StateManager.get_config('boss1', 'boss1_score'),
            health=StateManager.get_config('boss1', 'boss1_health'),
            power=1,
            typeid='stage2_boss1'
        )
        self.boss.add_event_listener('delete', self.stage_clear)
        self.boss.add_event_listener(
            'add_score', self.add_score, self.boss.score)
        self.enemies.add_entity(self.boss)

        # 보스 무기
        default_boss_weapon = DefaultStage2BossWeapon((40, 60))
        default_boss_weapon.bind_boss(self.boss)
        self.boss.set_weapon(default_boss_weapon)

        return True

    def game_over(self):
        self.end_stage()
        self.call_event('game_over')

    def stage_clear(self):
        self.end_stage()
        self.call_event('stage_clear')

    def end_stage(self):
        StateManager.set_config('player', 'health', self.player.health)
        self.timer_manager.clear_all_timers()
        self.items.clear_entities()
        self.bullets.clear_entities()
        self.enemies.clear_entities()

    # ------------------------------------------------ callbacks

    def add_score(self, adding_score: int):
        '''
        점수를 score만큼 증가시킨다
        '''
        StateManager.set_config(
            'global', 'score', self.get_score()+adding_score)

    def get_score(self):
        return StateManager.get_config('global', 'score')

    def update_enemy_speed(self):
        default_speed = StateManager.get_config('enemy', 'speed') // 3
        for enemy in self.enemies.array:
            direction = get_direction(enemy.pos, self.player.get_pos())
            enemy.speed = [direction[0] * default_speed,
                           direction[1] * default_speed]

    def move_player(self):
        '''
        플레이어를 keys를 통해 움직인다
        '''
        self.player.move(pygame.key.get_pressed())

    def move_entities(self):
        '''
        모든 엔티티를 자신의 속도로 움직인다.
        '''
        for enemy in self.enemies.array:
            enemy.move()
        for bullet in self.bullets.array:
            bullet.move()
        for item in self.items.array:
            item.move()

    def check_collide(self):
        '''
        플레이어와 엔티티의 충돌을 감지하고 이벤트를 처리한다
        '''
        player_rect = self.player.get_rect()

        # 적과 총알 충돌
        for bullet in self.bullets.array:
            for enemy in self.enemies.array:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    # increase score for attack
                    bullet.do_when_collide_with_enemy(enemy)

        # 플레이어와 아이템 충돌
        for item in self.items.array:
            if item.get_rect().colliderect(player_rect):
                item.do_when_collide_with_player(self.player)

        # 플레이어와 적 충톨
        for enemy in self.enemies.array:
            if enemy.get_rect().colliderect(player_rect):
                enemy.do_when_collide_with_player(self.player)

    def draw(self, screen: pygame.Surface):
        '''
        플레이어와 엔티티를 화면에 그린다
        '''

        # get config
        BACKGROUND = StateManager.get_config('stage2', 'background')
        TEXT_COLOR = StateManager.get_config('global', 'text_color')
        ENTITY_BOUNDARY: pygame.Rect = StateManager.get_config(
            'stage2', 'entity_boundary')
        temp_screen = pygame.Surface(
            (ENTITY_BOUNDARY.width, ENTITY_BOUNDARY.height))

        camera_rect = self.get_camera_rect()

        temp_screen.fill((255, 255, 255, 0))
        pygame.draw.rect(temp_screen, (0, 0, 0), ENTITY_BOUNDARY, width=5)
        self.player.draw(temp_screen)
        for bullet in self.bullets.array:
            bullet.draw(temp_screen)
        for item in self.items.array:
            item.draw(temp_screen)
        for enemy in self.enemies.array:
            enemy.draw(temp_screen)

        screen.blit(BACKGROUND, (0, 0))
        screen.blit(temp_screen, (0, 0), camera_rect)
        blit_text(
            screen=screen,
            msg=f'Score: {str(self.get_score()).zfill(6)}',
            color=TEXT_COLOR,
            center=(400, 10)
        )
        blit_text(
            screen=screen,
            msg=f'Health: {self.player.health}',
            color=TEXT_COLOR,
            center=(400, 40)
        )

        info_pos = list(screen.get_rect().midbottom)
        info_pos[1] -= 10
        blit_item(
            screen=screen,
            item=self.player.weapon.render_skill_info(),
            midbottom=info_pos
        )

    def get_camera_rect(self):
        camera_rect: pygame.Rect = StateManager.get_config(
            'global', 'screen_rect').copy()
        camera_rect.center = self.player.get_rect().center
        return camera_rect

    def update(self):
        '''
        매 프레임마다 실행되어 게임을 업데이트 한다
        '''
        # 시간에 따른 점수 증가
        self.add_score(1)

        # 점수에 따른 레벨업
        if self.get_score() >= self.next_level_score:
            self.when_level_up()

        # 엔티티 소환
        self.player.attack()
        self.item_summoner.summon()
        if self.boss:
            self.boss.attack()

        self.timer_manager.update()

        # 플레이어와 엔티티 업데이트
        if self.boss:
            self.boss.update()
        self.move_player()  # 플레이어 이동
        self.update_enemy_speed()
        self.move_entities()  # 엔티티 이동
        self.check_collide()  # 충돌 확인

        self.enemies.update()
        self.bullets.update()
        self.items.update()

    def when_level_up(self):
        fps = StateManager.get_config('global', 'fps')
        StateManager.set_config('global', 'fps', fps+1)
        self.next_level_score += self.level_interval
