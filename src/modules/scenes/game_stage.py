import pygame

from ...interfaces.object_configs import ConfigManager
from ...interfaces.scene import Scene
from ...interfaces.timer import *
from ...interfaces.entity_manager import EntityManager, EntityManagerFactory
from ..boss1 import Boss1
from ..bullet import Bullet
from ..enemy import Enemy
from ..item import Item
from ..player import Player
from ..player_weapon import *
from ..render_items import *


class GameStage(Scene):
    '''
    게임의 스테이지 하나
    스테이지를 시작학 때 start_scene 호출 필요
    게임이 끝날 때 EventListener.call_event('game_over')
    보스를 잡았을 때 EventListener.call_event('stage_clear')
    '''

    def __init__(
        self,
        level_interval: int,
        config_manager: ConfigManager
    ):
        '''
        level_interval: int | 레벨의 점수 간격
        '''
        super().__init__(config_manager)

        # 변수
        self.player = None
        self.boss: Boss1 = None
        self.list_enemies: list[Enemy] = []
        self.list_bullets: list[Bullet] = []
        self.list_items: list[Item] = []
        self.score = 0
        self.level_interval = level_interval
        self.next_level_score = level_interval

    def start_scene(self):
        self.player = Player(self.configs)
        # 플레이어 무기
        default_weapon = DefaultWeapon(
            cooltime=10, make_bullet=self.make_bullet)
        player_weapon = ShotgunDecorator(default_weapon, 30, self.make_shotgun)
        self.player.set_weapon(player_weapon)

        # 타이머
        self.timer_manager = TimerManager()
        enemy_timer = Timer()
        enemy_timer.set_timeout(0, self.make_enemy)
        self.timer_manager.set_timer(
            enemy_timer, 'stage1_enemy_timer', (5, 20))

        item_timer = Timer()
        item_timer.set_timeout(0, self.make_item)
        self.timer_manager.set_timer(item_timer, 'stage1_item_timer', (25, 50))

        boss_spell_timer = Timer()
        boss_spell_timer.set_timeout(0, self.make_boss_spell)
        self.timer_manager.set_timer(
            boss_spell_timer, 'stage1_boss_spell_timer', (35, 50))

        summon_boss_timer = Timer()
        summon_boss_timer.set_timeout(self.configs.get_config(
            'boss1', 'boss1_summon_delay'), self.summon_boss)
        self.timer_manager.set_timer(
            summon_boss_timer, 'stage1_summon_boss_timer', None)

        # add event_listener
        self.player.add_event_listener('delete', self.game_over)

    # callbacks ------------------------------------------------

    def make_enemy(self):
        '''
        callback of enemy_timer

        새로운 적을 생성한다
        self.ENEMY_IMAGES 중 랜덤 이미지를 사용한다
        '''
        # get config
        offset = self.configs.get_config('enemy', 'enemy_offset_width')
        screen_width = self.configs.get_config('global', 'screen_width')
        enemy_imgs = self.configs.get_config('enemy', 'imgs')
        enemyid = random.randint(0, len(enemy_imgs)-1)

        new_enemy = Enemy(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=enemy_imgs[enemyid],
            speed=(0, self.configs.get_config('enemy', 'speed')),
            boundary_rect=self.configs.get_config(
                'stage1', 'entity_boundary'),
            score=self.configs.get_config('enemy', 'score'),
            health=self.configs.get_config('enemy', 'health'),
            power=self.configs.get_config('enemy', 'power'),
            typeid=f'default{enemyid}'
        )
        new_enemy.add_event_listener('delete', self.delete_enemy, new_enemy)
        new_enemy.add_event_listener(
            'add_score', self.add_score, new_enemy.score)
        self.list_enemies.append(new_enemy)

        return True

    def make_bullet(self):
        '''
        callback of weapon
        새로운 총알을 생성한다
        '''

        # get config
        bullet_img: pygame.Surface = self.configs.get_config(
            'bullet', 'bullet_img')

        player_rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = bullet_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        new_bullet = Bullet(
            pos=img_rect.topleft,
            img=bullet_img,
            speed=(0, -self.configs.get_config('bullet', 'speed')),
            boundary_rect=self.configs.get_config(
                'stage1', 'entity_boundary'),
            power=self.player.power
        )
        new_bullet.add_event_listener(
            'delete', self.delete_bullet, new_bullet)
        self.list_bullets.append(new_bullet)

    def make_shotgun(self):
        '''
        callback of weapon
        새로운 총알 여러 개를 생성한다
        '''
        # get config
        shotgun_img: pygame.Surface = self.configs.get_config(
            'bullet', 'shotgun_img')

        player_rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = shotgun_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        speed = self.configs.get_config('bullet', 'speed')
        boundary_rect = self.configs.get_config(
            'stage1', 'entity_boundary')

        for i in range(-2, 3):
            new_rect = img_rect.copy()
            new_rect.left = img_rect.left + (img_rect.width + 10)*i

            new_bullet = Bullet(
                pos=new_rect.topleft,
                img=shotgun_img,
                speed=(i*2, -speed),
                boundary_rect=boundary_rect,
                power=self.player.power//4
            )
            new_bullet.add_event_listener(
                'delete', self.delete_bullet, new_bullet)
            self.list_bullets.append(new_bullet)

    def make_item(self):
        '''
        callback of item_timer
        '''

        # get config
        offset = self.configs.get_config('item', 'item_offset_width')
        screen_width = self.configs.get_config('global', 'screen_width')
        item_imgs = self.configs.get_config('item', 'imgs')

        new_item = Item(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=item_imgs[random.randint(0, len(item_imgs)-1)],
            speed=(0, self.configs.get_config('item', 'speed')),
            boundary_rect=self.configs.get_config(
                'stage1', 'entity_boundary'),
            heal=self.configs.get_config('item', 'heal')
        )
        new_item.add_event_listener('delete', self.delete_item, new_item)
        self.list_items.append(new_item)
        return True

    def make_boss_spell(self):
        if self.boss:  # boss가 존재하면
            new_spell: Enemy = self.boss.summon_spell()
            new_spell.add_event_listener(
                'delete', self.delete_enemy, new_spell)
            new_spell.add_event_listener('add_score', self.add_score, 0)
            self.list_enemies.append(new_spell)
            return True
        return False

    def summon_boss(self):
        img: pygame.Surface = self.configs.get_config('boss1', 'boss1_img')
        img_rect = img.get_rect()
        img_rect.top = 20
        img_rect.centerx = self.configs.get_config(
            'global', 'screen_rect').centerx
        self.boss = Boss1(
            self.configs,
            pos=img_rect.topleft,
            img=self.configs.get_config('boss1', 'boss1_img'),
            speed=(self.configs.get_config('boss1', 'boss1_speed'), 0),
            boundary_rect=self.configs.get_config('stage1', 'entity_boundary'),
            score=self.configs.get_config('boss1', 'boss1_score'),
            health=self.configs.get_config('boss1', 'boss1_health'),
            power=1000000,
            typeid='stage1_boss1'
        )
        self.boss.add_event_listener('delete', self.stage_clear)
        self.boss.add_event_listener(
            'add_score', self.add_score, self.boss.score)
        self.list_enemies.append(self.boss)
        return True

    def delete_enemy(self, enemy: Enemy):
        '''callback of add_event_listener('delete')'''
        self.list_enemies.pop(self.list_enemies.index(enemy))

    def delete_bullet(self, bullet: Bullet):
        '''callback of add_event_listener('delete')'''
        self.list_bullets.pop(self.list_bullets.index(bullet))

    def delete_item(self, item: Item):
        '''callback of add_event_listener('delete')'''
        self.list_items.pop(self.list_items.index(item))

    def add_score(self, adding_score: int):
        '''
        점수를 score만큼 증가시킨다
        '''
        self.score += adding_score

    def game_over(self):
        '''
        게임이 끝남을 설정하는 함수이다
        '''
        self.configs.set_config('global', 'score', self.score)
        self.call_event('game_over')

    def stage_clear(self):
        self.configs.set_config('global', 'score', self.score)
        self.configs.set_config('player', 'health', self.player.health)
        self.timer_manager.clear_all_timers()
        self.call_event('stage_clear')

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
        for enemy in self.list_enemies:
            enemy.move()
        for bullet in self.list_bullets:
            bullet.move()
        for item in self.list_items:
            item.move()

    def check_collide(self):
        '''
        플레이어와 엔티티의 충돌을 감지하고 이벤트를 처리한다
        '''
        player_rect = self.player.get_rect()

        # 적과 총알 충돌
        for enemy in self.list_enemies:
            for bullet in self.list_bullets:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    # increase score for attack
                    bullet.do_when_collide_with_enemy(enemy, self.add_score)

        # 플레이어와 아이템 충돌
        for item in self.list_items:
            if item.get_rect().colliderect(player_rect):
                item.do_when_collide_with_player(self.player)

        # 플레이어와 적 충톨
        for enemy in self.list_enemies:
            if enemy.get_rect().colliderect(player_rect):
                enemy.do_when_collide_with_player(self.player)

    def draw(self, screen: pygame.Surface):
        '''
        플레이어와 엔티티를 화면에 그린다
        '''

        # get config
        BACKGROUND = self.configs.get_config(
            'stage1', 'background')
        TEXT_COLOR = self.configs.get_config('global', 'text_color')

        screen.blit(BACKGROUND, (0, 0))
        self.player.draw(screen)
        for bullet in self.list_bullets:
            bullet.draw(screen)
        for item in self.list_items:
            item.draw(screen)
        for enemy in self.list_enemies:
            enemy.draw(screen)

        draw_text(
            screen=screen,
            msg=f'Score: {str(self.score).zfill(6)}',
            color=TEXT_COLOR,
            center=(400, 10)
        )
        draw_text(
            screen=screen,
            msg=f'Health: {self.player.health}',
            color=TEXT_COLOR,
            center=(400, 40)
        )

    def update(self):
        '''
        매 프레임마다 실행되어 게임을 업데이트 한다
        '''
        # 시간에 따른 점수 증가
        self.score += 1

        # 점수에 따른 레벨업
        if self.score >= self.next_level_score:
            fps = self.configs.get_config('global', 'fps')
            self.configs.set_config('global', 'fps', fps+1)
            self.next_level_score += self.level_interval

        # 랜덤 시간마다 적 생성
        # 일정 시간마다 총알 생성
        self.player.attack()
        self.timer_manager.update()

        # 플레이어와 엔티티 업데이트
        if self.boss:
            self.boss.update()
        self.move_player()  # 플레이어 이동
        self.move_entities()  # 엔티티 이동
        self.check_collide()  # 충돌 확인
