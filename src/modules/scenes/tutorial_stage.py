'첫 번째 스테이지'

import pygame
import time

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
from ..sprites.dialogue import Dialogue


class TutorialStage(Scene):
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
        self.enemy_summoner = None
        self.level_interval = level_interval
        self.next_level_score = level_interval
        self.grade = 0
        self.dialogue = None
        self.isplay = False
        self.end_dialogue = False

    def start_scene(self):
        '''
        tutorial_scene를 시작한다
        '''
        self.player = Player()
        self.enemies = EntityManagerFactory.get_manager('enemy')
        self.bullets = EntityManagerFactory.get_manager('bullet')
        self.items = EntityManagerFactory.get_manager('item')

        self.next_level_score = StateManager.get_score()+self.level_interval

        # 플레이어 무기
        default_weapon = DefaultPlayerWeapon(
            cooltime=10)
        player_weapon = ShotgunDecorator(default_weapon, 100)
        player_weapon.bind_player(self.player)
        self.player.set_weapon(player_weapon)

        # 소환자
        default_item_summoner = DefaultStage1ItemSummoner(
            cooltime_range=(25, 50),
            heal=StateManager.get_state('item', 'heal')
        )
        self.item_summoner = default_item_summoner

        default_enemy_summoner = DefaultStage1EnemySummoner(
            cooltime_range=(5, 20)
        )
        self.enemy_summoner = default_enemy_summoner

        # 타이머
        self.timer_manager = TimerManager()

        summon_boss_timer = Timer()
        summon_boss_timer.set_timeout(StateManager.get_state(
            'boss1', 'boss1_summon_delay'), self.summon_boss)
        self.timer_manager.set_timer(
            summon_boss_timer, 'stage0_summon_boss_timer', None)

        self.dialogue_timer = ManualTimer()
        self.timer_manager.set_manual_timer(
            self.dialogue_timer, 'stage0_dialogue_timer')

        # add event_listener
        self.player.add_event_listener('delete', self.game_over)

        # 대사
        self.dialogue = Dialogue(self.set_playing)
        self.dialogue.add_message("WASD로 움직여 보세요", 100)
        self.dialogue.add_message("SPACEBAR로 기본공격을 해보세요", 100)
        self.dialogue.add_message(
            "플레이어가 과제에 닿으면 과제를 시간 안에\n하지 못한 것으로 체력이 닳아요", 0)
        self.dialogue.add_message("총알이 과제에 맞으면 과제를 해결한 것으로\n학점이 올라요", 100)
        self.dialogue.add_message("보스가 쏘는 노란색 무기는\n총알이 닿아도 없어지지 않아요", 100)
        self.dialogue.add_message("E로 강한 공격을 해보세요", 100)
        self.dialogue.add_message(
            "오른쪽 위에 현재 학점과 체력이 표시돼요\n체력이 다 닳면 게임이 끝나요", 100)
        self.dialogue.add_message("보스의 체력이 다 닳면 다음 스테이지로 넘어갑니다", 100)

    # callbacks ------------------------------------------------

    def set_playing(self, is_playing):
        '2가 들어오면 대화 종료'
        if is_playing == 2:
            self.end_dialogue = True
            self.isplay = True
            return
        self.isplay = is_playing

    def summon_boss(self):
        '''
        boss entity를 추가한다
        '''
        img: pygame.Surface = StateManager.get_state('boss1', 'boss1_img')
        img_rect = img.get_rect()
        img_rect.top = 20
        img_rect.centerx = StateManager.get_state(
            'stage1', 'entity_boundary').centerx
        self.boss = Boss1(
            pos=img_rect.topleft,
            img=StateManager.get_state('boss1', 'boss1_img'),
            speed=(0, 0),
            boundary_rect=StateManager.get_state(
                'stage1', 'entity_boundary'),
            score=StateManager.get_state('boss1', 'boss1_score'),
            health=StateManager.get_state('boss1', 'boss1_health')//3,
            power=1000000,
            typeid='stage0_boss1'
        )
        self.boss.add_event_listener('delete', self.stage_clear)

        # 보스 무기
        default_boss_weapon = DefaultStage1BossWeapon((35, 50))
        default_boss_weapon.bind_boss(self.boss)
        self.boss.set_weapon(default_boss_weapon)

        self.enemies.add_entity(self.boss)
        return True

    def game_over(self):
        '''
        player의 체력이 0이 됐을 때 game_over event를 호출한다
        '''
        self.end_stage()
        self.call_event('game_over')

    def stage_clear(self):
        '''
        스테이지가 끝났을 때 stage_clear event를 호출한다
        '''
        self.end_stage()
        self.call_event('stage_clear')

    def end_stage(self):
        '''
        스테이지가 끝났을 때 모든 entity와 timer를 제거한다
        '''
        StateManager.set_state('player', 'health', self.player.health)
        StateManager.set_state('player', 'weapon', self.player.weapon)
        if self.grade == len(GRADE):
            StateManager.set_state('player', 'grade', GRADE[-1])
        else:
            StateManager.set_state('player', 'grade', GRADE[self.grade])
        self.timer_manager.clear_all_timers()
        self.items.clear_entities()
        self.bullets.clear_entities()
        self.enemies.clear_entities()

    # ------------------------------------------------ callbacks

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
        BACKGROUND = StateManager.get_state('stage1', 'background')

        screen.blit(BACKGROUND, (0, 0))
        self.player.draw(screen)
        for bullet in self.bullets.array:
            bullet.draw(screen)
        for item in self.items.array:
            item.draw(screen)
        for enemy in self.enemies.array:
            enemy.draw(screen)

        topright = screen.get_rect().topright
        '''
        score_bar와 health_bar를 화면에 blit한다
        '''
        blit_item(screen, self.render_score_bar(),
                  topright=(topright[0]-25, topright[1]+30))
        blit_item(screen, self.player.render_health_bar(),
                  topright=(topright[0]-5, topright[1]+30))

        info_pos = list(screen.get_rect().midbottom)
        info_pos[1] -= 10
        blit_item(
            screen=screen,
            item=self.player.weapon.render_skill_info(),
            midbottom=info_pos
        )

        if not self.isplay:
            self.dialogue.draw(screen)

    def render_score_bar(self):
        '''
        score_bar를 result에 blit 한다
        '''
        bar_width, bar_height = 16, 100
        bar = pygame.Surface((bar_width, bar_height))
        bar.fill((255, 255, 255))
        if self.grade == len(GRADE):
            pygame.draw.rect(bar, (0, 0, 255), [
                0, 0, bar_width, bar_height])
            text = render_text(GRADE[self.grade - 1], (0, 0, 0), 12)
        else:
            pygame.draw.rect(bar, (0, 0, 0), [
                0, 0, bar_width, bar_height], 2)
            pygame.draw.rect(bar, (0, 0, 255), [
                0, 0, bar_width, bar_height * (StateManager.get_score()-self.next_level_score+self.level_interval) // self.level_interval])
            bar = pygame.transform.rotate(bar, 180)
            text = render_text(GRADE[self.grade], (0, 0, 0), 12)

        result = pygame.Surface((32, 120))
        result.fill((255, 255, 255))
        blit_item(result, bar, midtop=result.get_rect().midtop)
        blit_item(result, text, midbottom=result.get_rect().midbottom)

        return result

    def update(self):
        '''
        매 프레임마다 실행되어 게임을 업데이트 한다
        '''
        if not self.end_dialogue and self.dialogue_timer.time <= 0:
            self.isplay = False

        if self.isplay:
            self.game_update()
        else:
            self.dialogue.update()

    def game_update(self):
        # 시간에 따른 점수 증가
        StateManager.add_score(1)

        # 점수에 따른 레벨업
        if StateManager.get_score() >= self.next_level_score:
            self.when_level_up()

        # 엔티티 소환
        self.player.attack()
        self.item_summoner.summon()
        self.enemy_summoner.summon()
        if self.boss:
            self.boss.attack()

        self.timer_manager.update()

        # 플레이어와 엔티티 업데이트
        if self.boss:
            self.boss.update()
        self.move_player()  # 플레이어 이동
        self.move_entities()  # 엔티티 이동
        self.check_collide()  # 충돌 확인

        self.enemies.update()
        self.bullets.update()
        self.items.update()

    def when_level_up(self):
        '''
        레벨업 했을 때 학점을 올린다
        '''
        self.grade += 1
        if self.grade > len(GRADE):
            self.grade = len(GRADE)
        self.next_level_score += self.level_interval
