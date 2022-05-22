import pygame


def render_text(msg: str, color: tuple[int, int, int]) -> pygame.Surface:
    '''
    문자열 msg를 color 색깔로 render해서 return한다
    '''
    font = pygame.font.Font(None, 24)
    return font.render(msg, True, color)


def blit_item(screen: pygame.Surface, item: pygame.Surface, **kwargs):
    '''
    kwargs에는 rect의 prop을 전달해야 한다
    ex) center = (10,100)
        left = 10, top = 100
    '''
    item_rect = item.get_rect()
    for k, v in kwargs.items():
        item_rect.__setattr__(k, v)
    screen.blit(item, item_rect)


def draw_text(screen: pygame.Surface, msg: str, color: tuple[int, int, int], **kwargs):
    '''
    kwargs에는 rect의 prop을 전달해야 한다
    ex) center = (10,100)
        left = 10, top = 100
    '''
    text: pygame.Surface = render_text(msg, color)
    blit_item(screen, text, **kwargs)
