'''
모든 object의 config interface를 정의한다
'''


from typing import Any


class Config():
    '''
    interface config
    '''

    def __init__(self, **kwargs):
        self.config: dict[str, Any] = {}
        for k, v in kwargs.items():
            self.set_config(k, v)

    def get_config(self, name: str):
        return self.config[name]

    def set_config(self, name: str, value):
        self.config[name] = value


class EnemyConfig(Config):
    '''
    imgs: tuple[pygame.Surface] | 이미지들
    speed: tuple[int, int] | 초기 속도
    boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
    enemy_offset_width: int | 적이 좌우 벽에서 떨어진 정도
    score: int | 적을 죽이면 얻는 점수
    health: int | 적의 체력
    power: int | 적에게 맞으면 닳는 체력
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BulletConfig(Config):
    '''
    imgs: tuple[pygame.Surface] | 이미지들
    speed: tuple[int, int] | 초기 속도
    boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ItemConfig(Config):
    '''
    imgs: tuple[pygame.Surface] | 이미지들
    speed: tuple[int, int] | 초기 속도
    boundary_rect: pygame.Rect | 경계 밖으로 벗어나면 삭제
    item_offset_width: int | 적이 좌우 벽에서 떨어진 정도
    heal: int | 플레이어가 얻는 체력
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GlobalConfig(Config):
    '''
    screen_width: int\r
    screen_height: int\r
    screen: pygame.Surface\r
    screen_rect: pygame.Rect\r
    enemy_offset_width: int # 적이 좌우 벽에서 떨어진 정도\r
    background: pygame.Surface\r
    text_color: tuple[int, int, int]\r
    score: int
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ConfigManager():
    '''
    여러개의 config를 관리한다\n
    global, enemy, bullet
    '''

    def __init__(self):
        self.configs: dict[str, Config] = {}

    def get_config(self, type: str, name: str):
        return self.configs[type].get_config(name)

    def set_config(self, type: str, name: str, value):
        self.configs[type].set_config(name, value)

    def add_config(self, type: str, config: Config):
        self.configs[type] = config
