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
            self.set_state(k, v)

    def get_state(self, name: str):
        return self.config[name]

    def set_state(self, name: str, value):
        self.config[name] = value


class StateManager():
    '''
    여러개의 config를 관리한다
    '''

    configs: dict[str, GameState] = {}

    @classmethod
    def get_state(cls, type: str, name: str):
        'configs에 Gamestate를 추가한다'
        return cls.configs[type].get_state(name)

    @classmethod
    def set_state(cls, type: str, name: str, value):
        'gamestate의 config 값을 정한다'
        cls.configs[type].set_state(name, value)

    @classmethod
    def add_state(cls, type: str, config: GameState):
        'configs에 Gamestate를 추가한다'
        cls.configs[type] = config

    # 많이 참조하는 state 함수로 만든다
    @classmethod
    def get_score(cls):
        'player의 score를 return'
        return cls.get_state('player', 'score')

    @classmethod
    def add_score(cls, adding_score):
        'score에 점수를 추가한다'
        cls.set_state('player', 'score', cls.get_score()+adding_score)

    @classmethod
    def get_gold(cls):
        return cls.get_state('player', 'gold')

    @classmethod
    def add_gold(cls, adding_gold):
        cls.set_state('player', 'gold', cls.get_gold()+adding_gold)

    def __new__(self):
        return StateManager
