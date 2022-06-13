'버튼과 버튼관리자를 정의한다'

import pygame

from .event_listener import EventListener
from .utils import *


class Button(EventListener):
    '클릭 시 EventListener.call_event("click") 실행'

    def __init__(self, btn_rect: pygame.Rect, btn_img: pygame.Surface = None, btn_hover_img: pygame.Surface = None):
        super().__init__()
        self.pos = btn_rect.topleft
        self.is_hovered = False
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

        if btn_hover_img is None:
            rect = btn_rect.copy()
            rect.topleft = (0, 0)
            canvas = pygame.Surface((rect.width, rect.height))
            canvas.fill((255, 255, 255))
            pygame.draw.rect(canvas, (0, 100, 200), rect,
                             width=rect.width//50+1)
            blit_text(canvas, "purchase", (0, 0, 0),
                      font_size=15, center=rect.center)
            self.hover_img = canvas
        else:
            self.hover_img = btn_hover_img

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
        self.is_hovered = False
        if self.get_rect().collidepoint(mouse_pos):
            if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
                self.call_event('click')
            else:
                self.is_hovered = True

    def draw(self, screen: pygame.Surface):
        if self.is_hovered:
            screen.blit(self.hover_img, self.pos)
        else:
            screen.blit(self.img, self.pos)


class ButtonManager():
    '버튼을 관리한다'

    buttons: list[Button] = []
    to_remove = set()

    @classmethod
    def add_button(cls, button):
        cls.buttons.append(button)

    @classmethod
    def remove_button(cls, button):
        cls.to_remove.add(button)

    @classmethod
    def add_buttons(cls, list_button):
        for button in list_button:
            cls.buttons.append(button)

    @classmethod
    def remove_buttons(cls, list_button):
        for button in list_button:
            cls.to_remove.add(button)

    @classmethod
    def update(cls):
        for button in cls.buttons:
            button.update()

        for button in cls.to_remove:
            cls.buttons.remove(button)
        cls.to_remove.clear()

    @classmethod
    def draw(cls, screen: pygame.Surface):
        for button in cls.buttons:
            button.draw(screen)
