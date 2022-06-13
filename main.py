'''
게임을 실행하는 main 코드가 있다
'''

# 1 - 모듈 임포트

import pygame

from src.interfaces.game_state import *
from src.modules.scene_manager import SceneManager
from src.modules.scenes.around_stage import AroundStage
from src.modules.scenes.finish_scene import FinishScene
from src.modules.scenes.game_stage import GameStage
from src.modules.scenes.open_scene import OpeningScene
from src.modules.scenes.shop_scene import ShopScene
from src.modules.weapons.player_weapon import *

pygame.init()
# 2.1 전역 상수
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()

# 3 - 그림과 효과음 삽입
try:
    # 3.1 - 그림 삽입
    player_img = pygame.image.load("./asset/img/player.jpg")
    player_img = pygame.transform.scale(player_img, (192//4, 250//4))
    book = pygame.image.load("./asset/img/book.png")
    book = pygame.transform.scale(book, (378//10, 267//10))
    computer = pygame.image.load("./asset/img/computer.png")
    computer = pygame.transform.scale(computer, (177//5, 115//5))
    note = pygame.image.load("./asset/img/note.png")
    note = pygame.transform.scale(note, (183//6, 205//6))
    asteroidimgs = (computer, book, note)
    gameover_image = pygame.image.load("./asset/img/gameover.jpg")

    bullet_imgs = (pygame.image.load("./asset/img/bullet01.png"),)
    start_image = (pygame.image.load("./asset/img/opening_scene.png"))
    start_image = pygame.transform.scale(
        start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bullet_img = pygame.image.load("./asset/img/bullet01.png")
    shotgun_img = pygame.image.load("./asset/img/shotgun01.png")

    energy_drink_img = pygame.image.load("./asset/img/energy-drink.png")
    energy_drink_img = pygame.transform.scale(
        energy_drink_img, (128//3, 128//3))
    item_imgs = (energy_drink_img,)

    boss1_spell_img = pygame.image.load("./asset/img/boss1_spell1.png")
    boss1_img = pygame.image.load("./asset/img/boss1.png")
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
state_manager = StateManager()

global_state = GameState(
    screen_width=480,
    screen_height=640,
    text_color=BLACK,
    fps=FPS,
    screen_rect=SCREEN_RECT
)
stage1_config = GameState(
    background=background,
    entity_boundary=SCREEN_RECT
)
stage2_config = GameState(
    background=background,
    entity_boundary=pygame.Rect(0, 0, 1000, 1000)
)
enemy_config = GameState(
    imgs=asteroidimgs,  # 이미지들
    speed=10,  # 초기 속도
    enemy_offset_width=5,  # 적이 좌우 벽에서 떨어진 정도
    score=20,  # 적을 죽이면 얻는 점수
    health=100,  # 적의 체력
    power=50  # 적에게 맞으면 닳는 체력
)
bullet_config = GameState(
    bullet_img=bullet_img,  # 총알 이미지
    shotgun_img=shotgun_img,  # 샷건 이미지
    speed=10,  # 초기 속도
)
item_config = GameState(
    imgs=item_imgs,  # 이미지들
    speed=10,  # 초기 속도
    item_offset_width=20,  # 아이템이 좌우 벽에서 떨어진 정도
    heal=30  # 플레이어가 얻는 체력
)
boss_config = GameState(
    spell_img=boss1_spell_img,
    spell_speed=10,
    spell_power=10,
    boss1_img=boss1_img,
    boss1_health=3000,
    boss1_score=2000,
    boss1_summon_delay=50,
    boss1_speed=20
)
player_config = GameState(
    pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT*3//4),
    img=player_img,
    speed=5,
    weapon=None,
    boundary_rect=SCREEN_RECT,
    score=0,
    power=100,
    gold=0,
    health=1000
)

state_manager.add_state('global', global_state)
state_manager.add_state('stage1', stage1_config)
state_manager.add_state('stage2', stage2_config)
state_manager.add_state('enemy', enemy_config)
state_manager.add_state('bullet', bullet_config)
state_manager.add_state('item', item_config)
state_manager.add_state('boss1', boss_config)
state_manager.add_state('player', player_config)


# scenes
scene_manager = SceneManager()

# opening_scene
opening_scene = OpeningScene(
    background=start_image
)

opening_scene.add_event_listener(
    'start_game', scene_manager.goto_scene, 'stage1')
scene_manager.add_scene('start_scene', opening_scene)

# stage1
stage1 = GameStage(
    level_interval=200,
)
stage1.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')
stage1.add_event_listener(
    'stage_clear', scene_manager.goto_scene, 'stage2')
scene_manager.add_scene('stage1', stage1)

# stage2
stage2 = AroundStage(
    level_interval=200,
)
stage2.add_event_listener(
    'game_over', scene_manager.goto_scene, 'finish_scene')
stage2.add_event_listener(
    'stage_clear', scene_manager.goto_scene, 'finish_scene')
scene_manager.add_scene('stage2', stage2)

# game_over_scene
finish_scene = FinishScene(
    score=0,
    background=gameover_image
)
scene_manager.add_scene('finish_scene', finish_scene)

# shop_scene
shop_scene = ShopScene(background=background)
scene_manager.add_scene('shop_scene', shop_scene)

# start with opening_scene
scene_manager.current_scene = opening_scene
scene_manager.next_scene = opening_scene

# StateManager.add_gold(10000)
# scene_manager.current_scene = shop_scene
# scene_manager.next_scene = shop_scene


# 7 game loop
while True:
    scene_manager.update()

    SCREEN.fill((255, 255, 255))
    scene_manager.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    fpsClock.tick(scene_manager.fps)
    pygame.display.update()
