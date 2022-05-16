# 1 - 모듈 임포트
import pygame
import random

# 2 - 게임 변수 초기화
# 2.1 - 게임 화면
pygame.init()
screen = pygame.display.set_mode((480, 640))

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
    screen.blit(text, textRect)


class Spaceship():
    def __init__(self, x, y, img):
        self.pos = [x, y]
        self.img = img

    def moveto(self, x, y):
        self.pos = [x, y]

    def get_rect(self):
        spaceshiprect = pygame.Rect(spaceship.img.get_rect())
        spaceshiprect.left = spaceship.pos[0]
        spaceshiprect.top = spaceship.pos[1]
        return spaceshiprect

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

    def get_rect(self):
        stonerect = pygame.Rect(self.img.get_rect())
        stonerect.left = self.pos[0]
        stonerect.top = self.pos[1]
        return stonerect

    def draw(self, screen):
        screen.blit(self.img, self.pos)


spaceship = Spaceship(0, 600, spaceshipimg)
list_asteroid = []

# 5 - 게임 루프
running = True
while running:
    # 6 - 화면을 그리기에 앞서 화면을 흰색으로 지우기
    screen.fill((255, 255, 255))

    # 7 - 키보드/마우스 이벤트
    for event in pygame.event.get():
        # X 버튼을 클릭하면 게임 종료
        if event.type == pygame.QUIT:
            exit()

    # 8 - 점수 증가, 게임속도 증가
    score += 1
    text(score, 400, 10)
    if score % 100 == 0:
        FPS += 2

    # 9 - 게임 요소 상태 변경
    position = pygame.mouse.get_pos()
    spaceship.moveto(position[0], 600)
    spaceship.draw(screen)

    # 9.2 - asteroids 추가하기
    asteroidtimer -= 10
    if asteroidtimer <= 0:
        list_asteroid.append(Asteroid(random.randint(
            5, 475), 0, asteroidimgs[random.randint(0, len(asteroidimgs)-1)]))
        asteroidtimer = random.randint(50, 200)

    for stone in list_asteroid:
        # 모든 asteroids 이동
        stone.move()

        # spaceship에 닿지 않을 때
        if stone.pos[1] > 640:
            del stone
            continue

        # spaceship에 닿을 때
        if stone.get_rect().colliderect(spaceship.get_rect()):
            landingsound.play()
            del stone
            running = False
            continue

        # asteroid 그리기
        stone.draw(screen)

    # 10 - 게임 속도
    fpsClock.tick(FPS)

    # 11 - 화면 전체 업데이트
    pygame.display.flip()

# 12 - 게임 종료 화면
screen.blit(gameover, (0, 0))
text(score, screen.get_rect().centerx, screen.get_rect().centery)
pygame.display.flip()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
