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


class ConfigManager():
    '''
    여러개의 config를 관리한다
    '''

    configs: dict[str, Config] = {}

    @classmethod
    def get_config(cls, type: str, name: str):
        return cls.configs[type].get_config(name)

    @classmethod
    def set_config(cls, type: str, name: str, value):
        cls.configs[type].set_config(name, value)

    @classmethod
    def add_config(cls, type: str, config: Config):
        cls.configs[type] = config

    def __new__(self):
        return ConfigManager
