'''
게임을 실행하는 main 코드가 있다
'''

# 1 - 모듈 임포트
import random

import pygame

from src.interfaces.object_configs import *
from src.interfaces.timer import Timer, TimerManager
from src.modules.bullet import Bullet
from src.modules.enemy import Enemy
from src.modules.player import Player
from src.modules.render_items import draw_text, blit_item

# 2 - 게임 변수 초기화
pygame.init()

# 2.1 전역 상수
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
ENEMY_OFFSET_WIDTH = 5  # 적이 좌우 벽에서 떨어진 정도

BACKGROUND_COLOR = (255, 255, 255)  # white
BLACK = (0, 0, 0)

# 2.2 시간 변수
FPS = 30
fpsClock = pygame.time.Clock()


# 3 - 그림과 효과음 삽입
try:
    # 3.1 - 그림 삽입
    spaceshipimg = pygame.image.load("./img/spaceship.png")
    asteroid0 = pygame.image.load("./img/asteroid00.png")
    asteroid1 = pygame.image.load("./img/asteroid01.png")
    asteroid2 = pygame.image.load("./img/asteroid02.png")
    asteroidimgs = (asteroid0, asteroid1, asteroid2)
    gameover = pygame.image.load("./img/gameover.jpg")
    bullet_imgs = (pygame.image.load("./img/bullet01.png"),)

    # 3.2 - 효과음 삽입
    takeoffsound = pygame.mixer.Sound("./audio/takeoff.wav")
    landingsound = pygame.mixer.Sound("./audio/landing.wav")
    takeoffsound.play()
except FileNotFoundError as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    exit(0)


# 6 class Game


class GameStage():
    '''
    게임의 스테이지 하나
    '''

    def __init__(
        self,
        enemy_images: tuple[pygame.Surface],
        bullet_images: tuple[pygame.Surface],
        level_interval: int,
        fps: int,
        player: Player
    ):
        '''
        enemy_images: tuple[pygame.Surface] | 적 이미지
        bullet_images: tuple[pygame.Surface] | 총알 이미지
        level_interval: int | 레벨의 점수 간격
        player_power: int | 플레이어의 공격력
        fps: int | 초기 fps
        '''

        # 변수
        self.player = player
        self.list_enemies: list[Enemy] = []
        self.list_bullets: list[Bullet] = []
        self.score = 0
        self.fps = fps
        self.running = True
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
        new_entity_config = EntityConfig(
            pos=(random.randint(ENEMY_OFFSET_WIDTH,
                                SCREEN_WIDTH-ENEMY_OFFSET_WIDTH), 0),
            img=self.enemy_images[random.randint(0, len(self.enemy_images)-1)],
            speed=[0, 10],
            boundary_rect=SCREEN_RECT
        )
        new_enemy = Enemy(
            entity_config=new_entity_config,
            score=20,
            health=100,
            power=50
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
        player_rect = self.player.get_rect()
        img_bullet = self.bullet_images[random.randint(
            0, len(self.bullet_images)-1)]

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = img_bullet.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        new_entity_config = EntityConfig(
            pos=img_rect.topleft,
            img=img_bullet,
            speed=[0, -10],
            boundary_rect=SCREEN_RECT
        )
        new_bullet = Bullet(
            entity_config=new_entity_config,
            power=self.player.power
        )
        new_bullet.add_event_listener('delete', self.delete_bullet, new_bullet)
        self.list_bullets.append(new_bullet)

        return True

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
        self.running = False
        landingsound.play()

    def check_collide(self):
        '''
        플레이어와 엔티티의 충돌을 감지하고 이벤트를 처리한다
        '''
        player_rect = self.player.get_rect()

        # 플레이어와 적 충톨
        for enemy in self.list_enemies:
            if enemy.get_rect().colliderect(player_rect):
                enemy.do_when_collide_with_player(self.player)

        # 적과 총알 충돌
        for enemy in self.list_enemies:
            for bullet in self.list_bullets:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    # increase score for attack
                    bullet.do_when_collide_with_enemy(enemy, self.add_score)

    def draw(self, screen: pygame.Surface):
        '''
        플레이어와 엔티티를 화면에 그린다
        '''
        screen.fill(BACKGROUND_COLOR)
        self.player.draw(screen)
        for enemy in self.list_enemies:
            enemy.draw(screen)
        for bullet in self.list_bullets:
            bullet.draw(screen)

        draw_text(
            screen=screen,
            msg=f'Score: {str(self.score).zfill(6)}',
            color=BLACK,
            center=(400, 10)
        )
        draw_text(
            screen=screen,
            msg=f'Health: {self.player.health}',
            color=BLACK,
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


# object config
player_config = PlayerConfig(
    pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4),
    img=spaceshipimg,
    speed=(5, 5),
    boundary_rect=SCREEN_RECT,
    power=35,
    health=100
)

player = Player(player_config)

game = GameStage(
    enemy_images=asteroidimgs,
    bullet_images=bullet_imgs,
    level_interval=50,
    fps=FPS,
    player=player
)

# 7 game loop
while game.running:

    fpsClock.tick(game.fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update()

    game.draw(SCREEN)
    pygame.display.flip()


# 8 finish screen
blit_item(SCREEN, gameover, topleft=(0, 0))
draw_text(
    screen=SCREEN,
    msg=f'Score: {str(game.score).zfill(6)}',
    color=BLACK,
    center=SCREEN_RECT.center
)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
