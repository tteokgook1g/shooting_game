# 1 - 모듈 임포트
import pygame
import random

# 2 - 게임 변수 초기화
# 2.1 - 게임 화면
pygame.init()
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
ENEMY_OFFSET_WIDTH = 5  # min offset for enemy

# 2.2 - 시간관련 변수
FPS = 30
fpsClock = pygame.time.Clock()
asteroidtimer = 0

# 2.3 소행성 위치 변수
asteroids = [[20, 0, 0]]

# 2.4 - 점수
score = 0

try:
    # 3 - 그림과 효과음 삽입
    # 3.1 - 그림 삽입
    spaceshipimg = pygame.image.load("./img/spaceship.png")
    asteroid0 = pygame.image.load("./img/asteroid00.png")
    asteroid1 = pygame.image.load("./img/asteroid01.png")
    asteroid2 = pygame.image.load("./img/asteroid02.png")
    asteroidimgs = (asteroid0, asteroid1, asteroid2)
    gameover = pygame.image.load("./img/gameover.jpg")

    # 3.2 - 효과음 삽입
    takeoffsound = pygame.mixer.Sound("./audio/takeoff.wav")
    landingsound = pygame.mixer.Sound("./audio/landing.wav")
    takeoffsound.play()
except Exception as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    exit(0)


# 4 - 점수 출력
def text(arg, x, y):
    font = pygame.font.Font(None, 24)
    text = font.render("Score: " + str(arg).zfill(6), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    SCREEN.blit(text, textRect)


class Spaceship():
    def __init__(self, x, y, img):
        self.pos = [x, y]
        self.img = img

    def moveto(self, x, y):
        self.pos = [x, y]

    def get_rect(self):
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen):
        screen.blit(self.img, self.pos)


class Asteroid():
    def __init__(self, x, y, img):
        self.pos = [x, y]
        self.img = img
        self.speed = [0, 10]

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        # delete if self is out of screen
        if not self.get_rect().colliderect(SCREEN_RECT):
            del self

    def get_rect(self):
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def do_when_collide(self, player):
        landingsound.play()
        del self

    def draw(self, screen):
        screen.blit(self.img, self.pos)


class Game():
    def __init__(self, enemy_images, level_interval, fps=30):
        # variables
        self.player = Spaceship(0, 600, spaceshipimg)
        self.list_entities = []
        self.score = 0
        self.fps = fps
        self.enemy_timer = 0
        self.running = True
        self.level_interval = level_interval

        # constants
        self.ENEMY_IMAGES = enemy_images

    def make_enemy(self):
        self.list_entities.append(Asteroid(
            random.randint(ENEMY_OFFSET_WIDTH,
                           SCREEN_WIDTH-ENEMY_OFFSET_WIDTH),
            0,
            self.ENEMY_IMAGES[random.randint(0, len(self.ENEMY_IMAGES)-1)]))

    def move_player(self, x, y):
        self.player.moveto(x, y)

    def move_enemies(self):
        for enemy in self.list_entities:
            enemy.move()

    def check_collide(self):
        player_rect = self.player.get_rect()
        for enemy in self.list_entities:
            if enemy.get_rect().colliderect(player_rect):
                enemy.do_when_collide(self.player)
                self.running = False

    def draw(self):
        self.player.draw(SCREEN)
        for enemy in self.list_entities:
            enemy.draw(SCREEN)

    def update(self):
        # 8 - 점수 증가, 게임속도 증가
        self.score += 1
        text(self.score, 400, 10)
        if self.score % self.level_interval == 0:
            self.fps += 2

        # 9 - 게임 요소 상태 변경
        pos = pygame.mouse.get_pos()
        self.move_player(pos[0], self.player.pos[1])

        self.enemy_timer -= 10
        if self.enemy_timer <= 0:
            self.make_enemy()
            self.enemy_timer = random.randint(50, 200)

        self.move_enemies()
        self.check_collide()
        self.draw()


game = Game(enemy_images=asteroidimgs, level_interval=50)

# 5 - 게임 루프
while game.running:
    # 6 - 화면을 흰색으로 지우기
    SCREEN.fill((255, 255, 255))

    # 7 - 키보드/마우스 이벤트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    game.update()
    # 10 - 게임 속도
    fpsClock.tick(game.fps)

    # 11 - 화면 전체 업데이트
    pygame.display.flip()

# 12 - 게임 종료 화면
SCREEN.blit(gameover, (0, 0))
text(game.score, SCREEN.get_rect().centerx, SCREEN.get_rect().centery)
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
