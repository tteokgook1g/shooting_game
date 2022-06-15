'버튼과 버튼관리자를 정의한다'

import pygame

from .event_listener import EventListener
from .utils import *


class Button(EventListener):
    '클릭 시 EventListener.call_event("click") 실행'

    def __init__(self, btn_rect: pygame.Rect, btn_img: pygame.Surface = None, btn_hover_img: pygame.Surface = None):
        '''
        btn_rect: pygame.Rect | 버튼의 위치, 크기
        btn_img: pygame.Surface | 이미지
        btn_hover_img | 마우스 커서가 btn_img 위에 올라갔을 때 변화하는 이미지
        '''
        super().__init__()
        self.pos = btn_rect.topleft
        self.is_hovered = False  # 마우스 커서가 button 위에 있는지 확인
        if btn_img is None:  # button 이미지가 없을 시 기본 이미지로 설정
            rect = btn_rect.copy()
            rect.topleft = (0, 0)
            canvas = pygame.Surface((rect.width, rect.height))
            canvas.fill((255, 255, 255))
            pygame.draw.rect(canvas, (0, 0, 0), rect, width=rect.width//50+1)
            blit_text(canvas, "button", (0, 0, 0), center=rect.center)
            self.img = canvas
        else:
            self.img = btn_img

        if btn_hover_img is None:  # button_hover_img 가 없을 경우 기본 이미지로 설정
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
        '''
        button 이 클릭되었을때 'click' 이벤트 실행한다
        '''
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = False
        if self.get_rect().collidepoint(mouse_pos):
            if pygame.event.peek(pygame.MOUSEBUTTONDOWN):
                self.call_event('click')
            else:
                self.is_hovered = True

    def draw(self, screen: pygame.Surface):
        '''
        button 이미지를 화면에 blit 한다
        '''
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
        '''
        buttons list 에 button 추가한다
        '''
        cls.buttons.append(button)

    @classmethod
    def remove_button(cls, button):
        '''
        buttons list에서 button 제거한다
        '''
        cls.to_remove.add(button)

    @classmethod
    def add_buttons(cls, list_button):
        '''
        buttons list에 두개 이상의 button 추가한다
        '''
        for button in list_button:
            cls.buttons.append(button)

    @classmethod
    def remove_buttons(cls, list_button):
        '''
        button list에서 두개 이상의 button 을 제거한다
        '''
        for button in list_button:
            cls.to_remove.add(button)

    @classmethod
    def update(cls):
        '''
        buttons list 에 있는 button들을 업데이트한다
        '''
        for button in cls.buttons:
            button.update()

        for button in cls.to_remove:
            cls.buttons.remove(button)
        cls.to_remove.clear()

    @classmethod
    def draw(cls, screen: pygame.Surface):
        '''
        buttons list 에 있는 button들을 blit한다
        '''
        for button in cls.buttons:
            button.draw(screen)
