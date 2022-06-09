'''
모든 object의 config interface를 정의한다
'''


from typing import Any


class GameState():
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


class StateManager():
    '''
    여러개의 config를 관리한다
    '''

    configs: dict[str, GameState] = {}

    @classmethod
    def get_config(cls, type: str, name: str):
        return cls.configs[type].get_config(name)

    @classmethod
    def set_config(cls, type: str, name: str, value):
        cls.configs[type].set_config(name, value)

    @classmethod
    def add_config(cls, type: str, config: GameState):
        cls.configs[type] = config

    # 많이 참조하는 state 함수로 만든다
    @classmethod
    def get_score(cls):
        return cls.get_config('player', 'score')

    @classmethod
    def add_score(cls, adding_score):
        cls.set_config('player', 'score', cls.get_score()+adding_score)

    @classmethod
    def get_gold(cls):
        return cls.get_config('player', 'gold')

    @classmethod
    def add_gold(cls, adding_gold):
        cls.set_config('player', 'gold', cls.get_gold()+adding_gold)

    def __new__(self):
        return StateManager
