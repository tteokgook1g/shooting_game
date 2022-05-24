import pygame

from ...interfaces.object_configs import *
from ...interfaces.scene import Scene
from ...interfaces.timer import *
from ..bullet import Bullet
from ..enemy import Enemy
from ..player import Player
from ..render_items import *


class GameStage(Scene):
    '''
    게임의 스테이지 하나
    게임이 끝날 때 EventListener.call_event('game_over')
    '''

    def __init__(
        self,
        enemy_images: tuple[pygame.Surface],
        bullet_images: tuple[pygame.Surface],
        level_interval: int,
        fps: int,
        player: Player,
        config_manager: ConfigManager
    ):
        '''
        enemy_images: tuple[pygame.Surface] | 적 이미지
        bullet_images: tuple[pygame.Surface] | 총알 이미지
        level_interval: int | 레벨의 점수 간격
        player_power: int | 플레이어의 공격력
        fps: int | 초기 fps
        '''
        super().__init__(config_manager)

        # 변수
        self.player = player
        self.list_enemies: list[Enemy] = []
        self.list_bullets: list[Bullet] = []
        self.score = 0
        self.fps = fps
        self.level_interval = level_interval
        self.next_level_score = level_interval

        # 타이머
        self.timer_manager = TimerManager()
        enemy_timer = Timer()
        enemy_timer.set_timeout(0, self.make_enemy)
        self.timer_manager.set_timer(enemy_timer, 'enemy_timer', (5, 20))

        bullet_timer = Timer()
        bullet_timer.set_timeout(0, self.make_bullet)
        self.timer_manager.set_timer(bullet_timer, 'bullet_timer', (10, 10))

        # 상수
        self.enemy_images = enemy_images
        self.bullet_images = bullet_images

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

        new_enemy = Enemy(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=enemy_imgs[random.randint(0, len(enemy_imgs)-1)],
            speed=self.configs.get_config('enemy', 'speed'),
            boundary_rect=self.configs.get_config(
                'global', 'screen_rect'),
            score=self.configs.get_config('enemy', 'score'),
            health=self.configs.get_config('enemy', 'health'),
            power=self.configs.get_config('enemy', 'power')
        )
        new_enemy.add_event_listener('delete', self.delete_enemy, new_enemy)
        new_enemy.add_event_listener(
            'add_score', self.add_score, new_enemy.score)
        self.list_enemies.append(new_enemy)

        return True

    def make_bullet(self):
        '''
        callback of bullet_timer

        새로운 총알을 생성한다
        self.BULLET_IMAGES 중 랜덤 이미지를 사용한다
        '''
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # get config
            bullet_imgs: tuple[pygame.Surface] = self.configs.get_config(
                'bullet', 'imgs')

            player_rect = self.player.get_rect()
            img_bullet = bullet_imgs[random.randint(0, len(bullet_imgs)-1)]

            # 총알이 플레이어을 중앙 위에 생기도록 설정
            img_rect = img_bullet.get_rect()
            img_rect.bottom = player_rect.top
            img_rect.centerx = player_rect.centerx

            new_bullet = Bullet(
                pos=img_rect.topleft,
                img=img_bullet,
                speed=self.configs.get_config('bullet', 'speed'),
                boundary_rect=self.configs.get_config(
                    'bullet', 'boundary_rect'),
                power=self.player.power
            )
            new_bullet.add_event_listener(
                'delete', self.delete_bullet, new_bullet)
            self.list_bullets.append(new_bullet)

            return True
        else:
            return False

    def delete_enemy(self, enemy: Enemy):
        '''callback of add_event_listener('delete')'''
        self.list_enemies.pop(self.list_enemies.index(enemy))

    def delete_bullet(self, bullet: Bullet):
        '''callback of add_event_listener('delete')'''
        self.list_bullets.pop(self.list_bullets.index(bullet))

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
            'global', 'background')
        TEXT_COLOR = self.configs.get_config('global', 'text_color')

        screen.blit(BACKGROUND, (0, 0))
        self.player.draw(screen)
        for enemy in self.list_enemies:
            enemy.draw(screen)
        for bullet in self.list_bullets:
            bullet.draw(screen)

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
            self.fps += 2
            self.next_level_score += self.level_interval

        # 랜덤 시간마다 적 생성
        # 일정 시간마다 총알 생성
        self.timer_manager.update()

        # 플레이어와 엔티티 업데이트
        self.move_player()  # 플레이어 이동
        self.move_entities()  # 엔티티 이동
        self.check_collide()  # 충돌 확인
