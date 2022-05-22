'''
class Timer
class TimerManager
'''

from typing import Callable
import random


class Timer():
    '''
    한 가지 작업에 대해 타이머를 설정하는 클래스
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


class TimerManager():
    '''
    타이머들을 관리한다
    '''

    def __init__(self):
        self.timers: dict[str, Timer] = {}
        self.frames_ranges: dict[str, tuple[int, int]] = {}

    def set_timer(self, timer: Timer, timer_name: str, frames_range: tuple[int, int]):
        '''
        timer를 timer_name으로 등록한다

        frames_range 범위에서 다음 실행 간격을 랜덤으로 설정한다
        범위 양 끝을 포함한다
        None을 입력하면 다시 실행하지 않는다
        '''
        self.timers[timer_name] = timer
        self.frames_ranges[timer_name] = frames_range

    def update(self):
        for timer_name in self.timers:
            timer = self.timers[timer_name]
            if timer.update():  # 콜백이 실행되면
                if self.frames_ranges[timer_name] is not None:  # 범위가 설정되어 있으면
                    timer.set_timeout(
                        random.randint(*self.frames_ranges[timer_name]),
                        timer.callback,
                        *timer.args,
                        **timer.kwargs
                    )
                else:  # 범위가 설정되어 있지 않으면
                    self.timers.pop(timer_name)
                    self.frames_ranges.pop(timer_name)