'''
게임을 실행하는 main 코드가 있다
'''

# 1 - 모듈 임포트

import pygame

from src.interfaces.object_configs import *
from src.modules.scene_manager import SceneManager
from src.modules.scenes.around_stage import AroundStage
from src.modules.scenes.finish_scene import FinishScene
from src.modules.scenes.game_stage import GameStage
from src.modules.scenes.open_scene import OpeningScene
from src.modules.weapons.player_weapon import *

pygame.init()
# 2.1 전역 상수
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
ENEMY_OFFSET_WIDTH = 5  # 적이 좌우 벽에서 떨어진 정도

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
    start_image = (pygame.image.load("./img/opening_scene.png"))
    start_image = pygame.transform.scale(
        start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bullet_img = pygame.image.load("./img/bullet01.png")
    shotgun_img = pygame.image.load("./img/shotgun01.png")
    item_imgs = (pygame.image.load("./img/item01.png"),)
    boss1_spell_img = pygame.image.load("./img/boss1_spell1.png")
    boss1_img = pygame.image.load("./img/boss1.png")
    boss1_img = pygame.transform.scale(boss1_img, (192//2, 250//2))

    # 3.2 - 효과음 삽입
except FileNotFoundError as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    exit(0)


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

global_config = Config(
    screen_width=480,
    screen_height=640,
    screen=SCREEN,
    screen_rect=SCREEN_RECT,
    text_color=BLACK,
    fps=FPS,
    score=0
)
stage1_config = Config(
    background=background,
    entity_boundary=SCREEN_RECT
)
stage2_config = Config(
    background=background,
    entity_boundary=pygame.Rect(0, 0, 1000, 1000)
)
enemy_config = Config(
    imgs=asteroidimgs,  # 이미지들
    speed=10,  # 초기 속도
    enemy_offset_width=5,  # 적이 좌우 벽에서 떨어진 정도
    score=20,  # 적을 죽이면 얻는 점수
    health=100,  # 적의 체력
    power=50  # 적에게 맞으면 닳는 체력
)
bullet_config = Config(
    bullet_img=bullet_img,  # 총알 이미지
    shotgun_img=shotgun_img,  # 샷건 이미지
    speed=10,  # 초기 속도
)
item_config = Config(
    imgs=item_imgs,  # 이미지들
    speed=10,  # 초기 속도
    item_offset_width=20,  # 아이템이 좌우 벽에서 떨어진 정도
    heal=10  # 플레이어가 얻는 체력
)
boss_config = Config(
    spell_img=boss1_spell_img,
    spell_speed=10,
    spell_power=10,
    boss1_img=boss1_img,
    boss1_health=3000,
    boss1_score=2000,
    boss1_summon_delay=50,
    boss1_speed=20
)
player_config = Config(
    pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4),
    img=player_img,
    speed=5,
    boundary_rect=SCREEN_RECT,
    weapon=None,
    power=100,
    health=20000
)

config_manager.add_config('global', global_config)
config_manager.add_config('stage1', stage1_config)
config_manager.add_config('stage2', stage2_config)
config_manager.add_config('enemy', enemy_config)
config_manager.add_config('bullet', bullet_config)
config_manager.add_config('item', item_config)
config_manager.add_config('boss1', boss_config)
config_manager.add_config('player', player_config)


# scenes
scene_manager = SceneManager(config_manager=config_manager)

# opening_scene
opening_scene = OpeningScene(
    config_manager=config_manager,
    background=start_image
)

opening_scene.add_event_listener(
    'start_game', scene_manager.goto_scene, 'stage1')
scene_manager.add_scene('start_scene', opening_scene)

# stage1
stage1 = GameStage(
    level_interval=200,
    config_manager=config_manager
)
stage1.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')
stage1.add_event_listener(
    'stage_clear', scene_manager.goto_scene, 'stage2')
scene_manager.add_scene('stage1', stage1)

# stage2
stage2 = AroundStage(
    level_interval=200,
    config_manager=config_manager
)
stage2.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')
stage2.add_event_listener(
    'stage_clear', scene_manager.goto_scene, 'finish_scene')
scene_manager.add_scene('stage2', stage2)

# game_over_scene
finish_scene = FinishScene(
    config_manager=config_manager,
    score=0,
    background=gameover_image
)
scene_manager.add_scene('finish_scene', finish_scene)

# start with opening_scene
scene_manager.current_scene = opening_scene
scene_manager.next_scene = opening_scene


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
