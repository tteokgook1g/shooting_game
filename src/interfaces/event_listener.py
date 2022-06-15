'''
interface event_listener
'''

from shutil import ExecError
from typing import Callable


class EventListener():
    '''
    raise ExecError when 존재하지 않는 이벤트 호출 시
    raise KeyError when 존재하지 않는 이벤트 삭제 시
    '''

    def __init__(self):
        self.event_listener = {}  # {event_name: (function, args, kwargs)}

    def call_event(self, event: str):
        '''
        함수에 입력된 event를 실행한다
        '''
        if event in self.event_listener:
            listener = self.event_listener[event]
            listener[0](*listener[1], **listener[2])
        else:
            raise ExecError

    def add_event_listener(self, event: str, callback: Callable, *args, **kwargs):
        '''
        event_listener에 함수를 추가한다
        '''
        self.event_listener[event] = (callback, args, kwargs)

    def delete_event_listener(self, event: str):
        'event_listener에서 함수를 제거한다'
        self.event_listener.pop(event)
