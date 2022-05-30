'''
게임을 실행하는 main 코드가 있다
'''

# 1 - 모듈 임포트

import pygame
from src.modules.player_weapon import *
from src.modules.scenes.start_scene import StartScene
from src.modules.scene_manager import SceneManager
from src.modules.scenes.finish_scene import FinishScene
from src.modules.scenes.open_scene import open_scene

from src.interfaces.object_configs import *
from src.modules.scenes.game_stage import GameStage
from src.modules.player import Player


pygame.init()
# 3 - 그림과 효과음 삽입
try:
    # 3.1 - 그림 삽입
    player_img = pygame.image.load("./img/player.jpg")
    player_img = pygame.transform.scale(player_img, (192//4, 250//4))
    asteroid0 = pygame.image.load("./img/asteroid00.png")
    asteroid1 = pygame.image.load("./img/asteroid01.png")
    asteroid2 = pygame.image.load("./img/asteroid02.png")
    asteroidimgs = (asteroid0, asteroid1, asteroid2)
    gameover_image = pygame.image.load("./img/gameover.jpg")

    bullet_imgs = (pygame.image.load("./img/bullet01.png"),)
    start_image = (pygame.image.load("./img/start_image.png"))

    bullet_img = pygame.image.load("./img/bullet01.png")
    shotgun_img = pygame.image.load("./img/shotgun01.png")
    item_imgs = (pygame.image.load("./img/item01.png"),)
    boss1_spell_img = pygame.image.load("./img/boss1_spell1.png")
    boss1_img = pygame.image.load("./img/boss1.png")
    boss1_img = pygame.transform.scale(boss1_img, (192//3, 250//3))

    # 3.2 - 효과음 삽입
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
    stage1_bg=background,
    text_color=BLACK,
    fps=FPS,
    score=0
)
enemy_config = EnemyConfig(
    imgs=asteroidimgs,
    speed=(0, 10),
    boundary_rect=SCREEN_RECT,
    enemy_offset_width=5,  # 적이 좌우 벽에서 떨어진 정도
    score=20,
    health=100,
    power=50
)
bullet_config = BulletConfig(
    bullet_img=bullet_img,
    shotgun_img=shotgun_img,
    speed=(0, -10),
    boundary_rect=SCREEN_RECT
)
item_config = ItemConfig(
    imgs=item_imgs,
    speed=(0, 10),
    boundary_rect=SCREEN_RECT,
    item_offset_width=20,
    heal=10
)
boss_config = Config(
    spell_img=boss1_spell_img,
    spell_speed=(0, 10),
    spell_power=10,
    boss1_img=boss1_img,
    boss1_health=500,
    boss1_score=2000,
    boss1_summon_delay=150,
    boss1_speed=(20, 0)
)

config_manager.add_config('global', global_config)
config_manager.add_config('enemy', enemy_config)
config_manager.add_config('bullet', bullet_config)
config_manager.add_config('item', item_config)
config_manager.add_config('boss1', boss_config)

# player
player = Player(
    pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4),
    img=player_img,
    speed=(5, 5),
    boundary_rect=SCREEN_RECT,
    weapon=None,
    power=50,
    health=200
)


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

start_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
start_bg.fill(WHITE)
start_scene = StartScene(
    config_manager=config_manager,
    background=start_bg
)
start_scene.add_event_listener(
    'start_game', scene_manager.goto_scene, 'stage1')
scene_manager.add_scene('start_scene', start_scene)

stage1 = GameStage(
    enemy_images=config_manager.get_config('enemy', 'imgs'),
    bullet_images=bullet_img,
    level_interval=200,
    player=player,
    config_manager=config_manager
)
stage1.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')
stage1.add_event_listener(
    'stage_clear', scene_manager.goto_scene, 'finish_scene')
scene_manager.add_scene('stage1', stage1)

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

scene_manager.add_scene('finish_scene', finish_scene)

scene_manager.current_scene = start_scene
scene_manager.next_scene = start_scene


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
