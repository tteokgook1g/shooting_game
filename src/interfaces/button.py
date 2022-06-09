'버튼과 버튼관리자를 정의한다'

import pygame

from .event_listener import EventListener
from .utils import *


class Button(EventListener):
    '클릭 시 EventListener.call_event("click") 실행'

    def __init__(self, btn_rect: pygame.Rect, btn_img: pygame.Surface = None):
        super().__init__()
        self.pos = btn_rect.topleft
        if btn_img is None:
            rect = btn_rect.copy()
            rect.topleft = (0, 0)
            canvas = pygame.Surface((rect.width, rect.height))
            canvas.fill((255, 255, 255))
            pygame.draw.rect(canvas, (0, 0, 0), rect, width=rect.width//50+1)
            blit_text(canvas, "button", (0, 0, 0), center=rect.center)
            self.img = canvas
        else:
            self.img = btn_img

    def get_rect(self):
        '''
        이것의 rect를 return한다
        '''
        rect = pygame.Rect(self.img.get_rect())
        rect.left = self.pos[0]
        rect.top = self.pos[1]
        return rect

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.get_rect().collidepoint(mouse_pos) and pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            self.call_event('click')

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.pos)


class ButtonManager():
    '버튼을 관리한다'

    def __init__(self):
        self.buttons: list[Button] = []
        self.to_remove = set()

    def add_button(self, button):
        self.buttons.append(button)

    def remove_button(self, button):
        self.to_remove.add(button)

    def add_buttons(self, list_button):
        for button in list_button:
            self.buttons.append(button)

    def remove_buttons(self, list_button):
        for button in list_button:
            self.to_remove.add(button)

    def update(self):
        for button in self.buttons:
            button.update()

        for button in self.to_remove:
            self.buttons.remove(button)
        self.to_remove.clear()

    def draw(self, screen: pygame.Surface):
        for button in self.buttons:
            button.draw(screen)
