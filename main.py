'''
게임을 실행하는 main 코드가 있다
'''

# 1 - 모듈 임포트

import pygame
from src.modules.scene_manager import SceneManager
from src.modules.scenes.finish_scene import FinishScene
from src.modules.scenes.open_scene import open_scene

from src.interfaces.object_configs import *
from src.modules.scenes.game_stage import GameStage
from src.modules.player import Player
# 2 - 게임 변수 초기화
pygame.init()
# 3 - 그림과 효과음 삽입
try:
    # 3.1 - 그림 삽입
    spaceshipimg = pygame.image.load("./img/spaceship.png")
    asteroid0 = pygame.image.load("./img/asteroid00.png")
    asteroid1 = pygame.image.load("./img/asteroid01.png")
    asteroid2 = pygame.image.load("./img/asteroid02.png")
    asteroidimgs = (asteroid0, asteroid1, asteroid2)
    gameover_image = pygame.image.load("./img/gameover.jpg")
    bullet_imgs = (pygame.image.load("./img/bullet01.png"),)
    start_image = (pygame.image.load("./img/start_image.png"))
    # 3.2 - 효과음 삽입
    takeoffsound = pygame.mixer.Sound("./audio/takeoff.wav")
    landingsound = pygame.mixer.Sound("./audio/landing.wav")
    takeoffsound.play()
except FileNotFoundError as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    exit(0)


# 2.1 전역 상수
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
ENEMY_OFFSET_WIDTH = 5  # 적이 좌우 벽에서 떨어진 정도  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(WHITE)


# 2.2 시간 변수
FPS = 30
fpsClock = pygame.time.Clock()


# 6 class Game


# object config
config_manager = ConfigManager()
global_config = GlobalConfig(
    screen_width=480,
    screen_height=640,
    screen=SCREEN,
    screen_rect=SCREEN_RECT,
    background=background,
    text_color=BLACK,
    fps=FPS,
    score=0
)
enemy_config = EnemyConfig(
    imgs=asteroidimgs,
    speed=(0, 10),
    boundary_rect=SCREEN_RECT,
    enemy_offset_width=5,
    score=20,
    health=100,
    power=50
)
bullet_config = BulletConfig(
    imgs=(bullet_imgs),
    speed=(0, -10),
    boundary_rect=SCREEN_RECT
)

config_manager.add_config('global', global_config)
config_manager.add_config('enemy', enemy_config)
config_manager.add_config('bullet', bullet_config)


# scenes
scene_manager = SceneManager(config_manager=config_manager)
opening_scene = open_scene(
    config_manager=config_manager,
    background=start_image
)
stage1 = GameStage(
    enemy_images=config_manager.get_config('enemy', 'imgs'),
    bullet_images=bullet_imgs,
    level_interval=50,
    fps=FPS,
    player=Player(
        pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4),    
        img=spaceshipimg,
        speed=(5, 5),
        boundary_rect=SCREEN_RECT,     
        power=35,
        health=100
    ),
    config_manager=config_manager
)
finish_scene = FinishScene(
    config_manager=config_manager,
    score=0,
    background=gameover_image
)
scene_manager.add_scene("opening_scene",opening_scene)
scene_manager.add_scene('stage1', stage1)
scene_manager.add_scene('finish_scene', finish_scene)
scene_manager.current_scene = opening_scene
scene_manager.next_scene = opening_scene

opening_scene.add_event_listener(
    'staet_game', scene_manager.goto_scene,'stage1'
)
stage1.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')

# 7 game loop
while True:

    fpsClock.tick(scene_manager.fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    scene_manager.update()

    scene_manager.draw(SCREEN)
    pygame.display.flip()
