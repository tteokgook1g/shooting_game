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

    def __init__(self):
        self.configs: dict[str, Config] = {}

    def get_config(self, type: str, name: str):
        return self.configs[type].get_config(name)

    def set_config(self, type: str, name: str, value):
        self.configs[type].set_config(name, value)

    def add_config(self, type: str, config: Config):
        self.configs[type] = config
