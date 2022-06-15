'''
class Timer
class TimerManager
'''

from typing import Callable
import random


class Timer():
    '''
    한 가지 작업에 대해 타이머를 설정하는 클래스
    시간이 지나면 콜백을 실행한다
    '''

    def __init__(self):
        self.time: int = 0  # 남은 프레임 수
        self.callback: Callable = None

    def set_timeout(self, frames: int, callback: Callable, *args, **kwargs):
        '''
        frames 이후에 callback(*args, **kwargs) 실행한다
        callback은 실행되었을 때 True 반환해야 한다
        '''
        self.callback = callback
        self.time = frames
        self.args = args
        self.kwargs = kwargs

    def update(self):
        '''
        콜백이 실행되면 True 리턴
        '''
        self.time -= 1
        if self.time <= 0:  # 시간이 지났으면
            return self.callback(*self.args, **self.kwargs)
        return False


class ManualTimer:
    '시간이 지나는 것만 계산하고 콜백은 실행하지 않는다'

    def __init__(self):
        self.time: int = 0  # 남은 프레임 수

    def set_timeout(self, frames: int):
        self.time = frames

    def update(self):
        self.time -= 1


class TimerManager():
    '''
    타이머들을 관리한다
    전역에 단 하나의 객체만 존재한다
    '''

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        '''
        timers | Timer를 저장한다
        manual_timers | ManualTimer를 저장한다
        frames_ranges | 랜덤으로 실행될 실행 간격을 결정하는 frames_range들을 저장한다
        '''
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.timers: dict[str, Timer] = {}
            self.manual_timers: dict[str, ManualTimer] = {}
            self.frames_ranges: dict[str, tuple[int, int]] = {}
            cls._init = True

    def set_timer(self, timer: Timer, timer_name: str, frames_range: tuple[int, int]):
        '''
        timer를 timer_name으로 등록한다

        frames_range 범위에서 다음 실행 간격을 랜덤으로 설정한다
        범위 양 끝을 포함한다
        None을 입력하면 다시 실행하지 않는다
        '''
        self.timers[timer_name] = timer
        self.frames_ranges[timer_name] = frames_range

    def get_timer(self, timer_name):
        '''
        timers에 timer를 추가한다
        '''
        if timer_name in self.timers:
            return self.timers[timer_name]
        if timer_name in self.manual_timers:
            return self.manual_timers[timer_name]

    def remove_timer(self, timer_name):
        '''
        timers에서 timer를 제거한다
        '''
        if timer_name in self.timers:
            self.timers.pop(timer_name)
        if timer_name in self.manual_timers:
            self.manual_timers.pop(timer_name)

    def set_manual_timer(self, timer: ManualTimer, timer_name: str):
        'timer를 timer_name으로 등록한다'
        self.manual_timers[timer_name] = timer

    def clear_all_timers(self):
        '''
        모든 timer를 제거한다
        '''
        self.timers.clear()
        self.manual_timers.clear()
        self.frames_ranges.clear()

    def update(self):
        for timer_name in self.timers.copy():
            timer = self.timers[timer_name]
            if timer.update():  # 콜백이 실행되면
                # 범위가 설정되어 있으면 timer를 설정한다
                if self.frames_ranges[timer_name] is not None:
                    timer.set_timeout(
                        random.randint(*self.frames_ranges[timer_name]),
                        timer.callback,
                        *timer.args,
                        **timer.kwargs
                    )
                else:  # 범위가 설정되어 있지 않으면 timers에서 제거한다
                    self.timers.pop(timer_name)
                    self.frames_ranges.pop(timer_name)

        for timer_name in self.manual_timers.copy():
            self.manual_timers[timer_name].update()
