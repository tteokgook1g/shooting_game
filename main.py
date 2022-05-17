# 1 - 모듈 임포트
import pygame
import random

# 2 - 게임 변수 초기화
pygame.init()

# 2.1 global constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_RECT = SCREEN.get_rect()
ENEMY_OFFSET_WIDTH = 5  # min offset for enemy

RED = (255, 0, 0)

# 2.2 variables about time
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
    bullet_images = (pygame.image.load("./img/bullet01.png"),)

    # 3.2 - 효과음 삽입
    takeoffsound = pygame.mixer.Sound("./audio/takeoff.wav")
    landingsound = pygame.mixer.Sound("./audio/landing.wav")
    takeoffsound.play()
except Exception as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    pygame.quit()
    exit(0)


# 4 blit text
def text(arg, x, y):
    font = pygame.font.Font(None, 24)
    text = font.render("Score: " + str(arg).zfill(6), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = x
    textRect.centery = y
    SCREEN.blit(text, textRect)

# 5 class of game objects

# 5.1 class Player


class Player():
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], boundary_rect: pygame.Rect, power: int):
        '''
        pos: (x, y) | initial position
        img: pygame.Surface | image
        speed: (speed_x, speed_y) | initial speed
        boundary_rect: pygame.Rect | boundary
        power: int | attack power
        '''

        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.boundary_rect = boundary_rect
        self.power = power

    def moveto(self, x, y):
        self.pos = [x, y]
        self.check_boundary()

    def move(self, keys):
        prev = self.pos[:]
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed[0]
        if keys[pygame.K_d]:
            self.pos[0] += self.speed[0]
        if keys[pygame.K_w]:
            self.pos[1] -= self.speed[1]
        if keys[pygame.K_s]:
            self.pos[1] += self.speed[1]

        if prev != self.pos:
            self.check_boundary()

    def check_boundary(self):
        player_rect = self.get_rect()
        left = self.boundary_rect.left
        right = self.boundary_rect.right - player_rect.width
        top = self.boundary_rect.top
        bottom = self.boundary_rect.bottom - player_rect.height

        if self.pos[0] < left:
            self.pos[0] = left
        elif self.pos[0] > right:
            self.pos[0] = right
        if self.pos[1] < top:
            self.pos[1] = top
        elif self.pos[1] > bottom:
            self.pos[1] = bottom

    def get_rect(self):
        rect = self.img.get_rect()
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)

# 5.2 non-player interface


class Entity():
    '''
    MUST OVERRIDE do_when_collide_with_player(self, player)
    '''

    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], func_delete):
        self.pos = list(pos[:])
        self.img = img
        self.speed = list(speed[:])
        self.delete = func_delete

    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        # delete if self is out of screen
        if not self.get_rect().colliderect(SCREEN_RECT):
            self.delete(self)

    def get_rect(self):
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)


# 5.3 class Enemy


class Enemy(Entity):
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], func_delete, score: int, health=100):
        super().__init__(pos, img, speed, func_delete)
        self.health = health
        self.score = score

    def do_when_collide_with_player(self, player: Player):
        landingsound.play()
        self.delete(self)

    def attacked(self, power: int):
        '''
        it returns score for attack
        enemy is attacked by power
        '''
        self.health -= power
        # delete when health <= 0
        if self.health <= 0:
            self.delete(self)
            return self.score
        return 0


# 5.4 class Bullet


class Bullet(Entity):
    def __init__(self, pos: tuple[int], img: pygame.Surface, speed: tuple[int], power: int, func_delete):
        super().__init__(pos, img, speed, func_delete)
        self.power = power  # attack power

    def do_when_collide_with_player(self, player: Player):
        ''' '''  # overrided
        pass  # do nothing

    def do_when_collide_with_enemy(self, enemy: Enemy):
        '''
        it returns score for attack
        '''
        self.delete(self)
        return enemy.attacked(self.power)

# 6 class Game


class Game():
    def __init__(self, enemy_images: tuple[pygame.Surface], bullet_images: tuple[pygame.Surface], level_interval: int, player_power: int, fps=30):
        # variables
        self.player = Player(pos=(200, 600), img=spaceshipimg,
                             speed=(5, 5), boundary_rect=SCREEN_RECT, power=player_power)
        self.list_enemies: list[Enemy] = []
        self.list_bullets: list[Bullet] = []
        self.score = 0
        self.fps = fps
        self.running = True
        self.level_interval = level_interval
        self.next_level_score = level_interval

        # timers
        self.enemy_timer = 0
        self.bullet_timer = 0

        # constants
        self.ENEMY_IMAGES = enemy_images
        self.BULLET_IMAGES = bullet_images

    def make_enemy(self):
        self.list_enemies.append(Enemy(
            pos=(random.randint(ENEMY_OFFSET_WIDTH,
                                SCREEN_WIDTH-ENEMY_OFFSET_WIDTH), 0),
            img=self.ENEMY_IMAGES[random.randint(0, len(self.ENEMY_IMAGES)-1)],
            speed=[0, 10],
            func_delete=self.delete_enemy,
            score=200))

    def make_bullet(self):
        pl_rect = self.player.get_rect()
        img_bullet = self.BULLET_IMAGES[random.randint(
            0, len(self.BULLET_IMAGES)-1)]

        img_rect = img_bullet.get_rect()
        img_rect.bottom = pl_rect.top
        img_rect.centerx = pl_rect.centerx

        self.list_bullets.append(Bullet(
            pos=img_rect.topleft,
            img=img_bullet,
            speed=[0, -10],
            power=self.player.power,
            func_delete=self.delete_bullet))

    # callback of delete
    def delete_enemy(self, enemy):
        self.list_enemies.pop(self.list_enemies.index(enemy))

    # callback of delete
    def delete_bullet(self, bullet):
        self.list_bullets.pop(self.list_bullets.index(bullet))

    def move_player(self, keys):
        self.player.move(keys)

    def move_entities(self):
        for enemy in self.list_enemies:
            enemy.move()
        for bullet in self.list_bullets:
            bullet.move()

    def check_collide(self):
        player_rect = self.player.get_rect()
        for enemy in self.list_enemies:
            if enemy.get_rect().colliderect(player_rect):
                enemy.do_when_collide_with_player(self.player)
                self.running = False

            for bullet in self.list_bullets:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    # increase score for attack
                    self.score += bullet.do_when_collide_with_enemy(enemy)

    def draw(self):
        self.player.draw(SCREEN)
        for enemy in self.list_enemies:
            enemy.draw(SCREEN)
        for bullet in self.list_bullets:
            bullet.draw(SCREEN)

    def update(self):
        # increase score
        self.score += 1
        text(self.score, 400, 10)

        # level up
        if self.score >= self.next_level_score:
            self.fps += 2
            self.next_level_score += self.level_interval

        # make enemy
        self.enemy_timer -= 10
        if self.enemy_timer <= 0:
            self.make_enemy()
            self.enemy_timer = random.randint(50, 200)

        # make bullet
        self.bullet_timer -= 10
        if self.bullet_timer <= 0:
            self.make_bullet()
            self.bullet_timer = 100

        # update game objects
        self.move_player(pygame.key.get_pressed())
        self.move_entities()
        self.check_collide()
        self.draw()


game = Game(enemy_images=asteroidimgs, bullet_images=bullet_images,
            level_interval=50, player_power=35, fps=FPS)

# 7 game loop
while game.running:
    SCREEN.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update()
    fpsClock.tick(game.fps)
    pygame.display.flip()

# 8 finish screen
SCREEN.blit(gameover, (0, 0))
text(game.score, SCREEN.get_rect().centerx, SCREEN.get_rect().centery)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)