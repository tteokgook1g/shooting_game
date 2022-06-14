'튜토리얼에 사용할 대화'

import pygame

from ...interfaces.timer import TimerManager
from ...interfaces.utils import *


class Dialogue():
    def __init__(self, func_toggle_playing):
        self.msg: list[tuple[str, int]] = []  # 메세지들을 저장 (msg, time interval)
        self.play_idx: list[int] = []
        self.curr_idx = 0  # 현재 메세지
        self.toggle_playing = func_toggle_playing

    def add_message(self, msg: str, time_interval: int):
        self.msg.append((msg, time_interval))
        if time_interval > 0:
            self.play_idx.append(len(self.msg)-1)

    def update(self):
        if pygame.event.peek(pygame.KEYDOWN):
            if self.curr_idx in self.play_idx:
                self.play_idx.remove(self.curr_idx)
                TimerManager().get_timer(
                    'stage0_dialogue_timer').time = self.msg[self.curr_idx][1]
                self.toggle_playing(True)

            self.curr_idx += 1
            if self.curr_idx >= len(self.msg):
                self.toggle_playing(2)
                TimerManager().remove_timer('stage0_dialogue_timer')

    def draw(self, screen: pygame.Surface):
        gap_height = 5
        font_size = 20
        sentences = self.msg[self.curr_idx][0].split('\n')
        sentence_height = render_text(
            " ", (0, 0, 0), font_size).get_rect().height
        curr_height = 0

        result = pygame.Surface(
            (480, sentence_height*len(sentences)+gap_height*(len(sentences)-1)), pygame.SRCALPHA)
        result.fill((255, 255, 255, 0))
        for m in sentences:
            result.blit(render_text(m, (0, 0, 0), font_size, (255, 255, 255)),
                        (0, curr_height))
            curr_height += gap_height + sentence_height

        btmleft = screen.get_rect().bottomleft
        blit_item(screen, result, bottomleft=(btmleft[0]+10, btmleft[1]-70))
