'''
다양한 무기 클래스를 정의한다.
'''

import pygame
from pygame import Vector2

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ...interfaces.timer import ManualTimer, TimerManager
from ...interfaces.utils import *
from ..sprites.bullet import Bullet


class PlayerWeapon():
    'interface weapon'

    def __init__(self):
        self.player = None
        self.bullets = EntityManagerFactory.get_manager('bullet')
        self.COLOR_DEACTIVATED = pygame.color.Color(150, 150, 150, 100)

        self.power = 0.0  # 현재 공격력

    def attack(self):
        pass

    def bind_player(self, player):
        '''
        playerweapon 에 대응되는 player를 bind 한다
        '''
        self.player = player

    def _render_skill_info_list(self):
        return []

    def render_skill_info(self):
        '''
        스킬의 리스트를 반환한다
        이 함수에서 _render_skill_info_list는 부모 클래스의 함수를 불러온다
        '''
        gap_width = 10
        infos: list[pygame.Surface] = self._render_skill_info_list()
        screen_width = sum(map(lambda x: x.get_rect().width,
                           infos))+gap_width*(len(infos)-1)
        screen_height = max(
            map(lambda x: x.get_rect().height, infos))

        result = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        result.fill((255, 255, 255))

        curr_point = Vector2(0, 0)

        for info in infos:
            result.blit(info, curr_point[:])
            curr_point.x += gap_width+info.get_rect().width

        return result


class WeaponDecorator(PlayerWeapon):
    'interface WeaponDecorator'

    def __init__(self, weapon: PlayerWeapon) -> None:
        '''
        weapon: PlayerWeapon | shotgun
        _weapon: PlayerWeapon | defaultweapon
        '''
        super().__init__()
        self._weapon = weapon

    def attack(self):
        '''
        기본 weapon의 공격을 수행한다
        '''
        self._weapon.attack()

    def bind_player(self, player):
        '''
        shotgun 과 defaultweapon과 player를 bind 해준다
        '''
        super().bind_player(player)
        self._weapon.bind_player(player)

    def _render_skill_info_list(self):
        '''
        defaultweapon의 skill_info_list를 호출한다
        '''
        return self._weapon._render_skill_info_list()


class DefaultPlayerWeapon(PlayerWeapon):
    '''
    spacebar로 쿨타임마다 공격한다.
    '''

    def __init__(self, cooltime: int):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_player_weapon')

        self.cooltime = cooltime

        self.power = 100.0
        self.sound = StateManager.get_state('bullet', 'default_bullet_sound')

    def attack(self):
        '''
        새로운 총알을 생성한다
        '''
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.sound.play()
            self.make_bullet()
            self.timer.time = self.cooltime

    def make_bullet(self):
        '''
        callback of weapon
        새로운 총알을 생성한다
        '''

        # get config
        bullet_img: pygame.Surface = StateManager.get_state(
            'bullet', 'bullet_img')
        bullet_img = pygame.transform.scale(bullet_img, (30, 30))

        player_rect: pygame.Rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = bullet_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        new_bullet = Bullet(
            pos=img_rect.topleft,
            img=bullet_img,
            speed=(0, -StateManager.get_state('bullet', 'speed')),
            boundary_rect=StateManager.get_state(
                'stage2', 'entity_boundary'),
            power=self.power
        )
        new_bullet.add_event_listener(
            'delete', self.delete_bullet, new_bullet)
        self.bullets.add_entity(new_bullet)

    def delete_bullet(self, bullet):
        '''
        bullet을 삭제한다
        '''
        self.bullets.remove_entity(bullet)

    def _render_skill_info_list(self):
        '''
        skill_info_list를 반환한다
        부모 클래스에서 _render_shop_info_list 함수를 불러온다
        '''
        bullet_img: pygame.Surface = StateManager.get_state(
            'bullet', 'bullet_img')
        bullet_img = pygame.transform.scale(bullet_img, (50, 50))

        if self.timer.time > 0:  # 비활성화 표시
            temp = pygame.Surface((50, 50), pygame.SRCALPHA)
            temp.fill(self.COLOR_DEACTIVATED)
            bullet_img.blit(temp, (0, 0))

            cooltime_text = render_text(
                f'{self.timer.time}', StateManager.get_state('global', 'text_color'), 16)
            blit_item(bullet_img, cooltime_text, bottomright=(50, 50))

        other = super()._render_shop_info_list()
        other.append(bullet_img)

        return other


class ShotgunDecorator(WeaponDecorator):

    def __init__(self, weapon: PlayerWeapon, cooltime: int):
        super().__init__(weapon)

        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'player_shotgun')

        self.cooltime = cooltime

        self.power = 100.0
        self.sound = StateManager.get_state('bullet', 'shotgun_sound')

    def attack(self):
        '''
        shotgun의 attack을 실행하고,
        super().attack에서 default_weapon의 attack을 실행한다
        '''
        super().attack()
        if self.timer.time <= 0 and pygame.key.get_pressed()[pygame.K_e]:
            self.make_shotgun()
            self.sound.play()
            self.timer.time = self.cooltime

    def make_shotgun(self):
        '''
        callback of weapon
        새로운 총알 여러 개를 생성한다
        '''
        NUM_OF_BULLET = 24

        # get config
        shotgun_img: pygame.Surface = StateManager.get_state(
            'bullet', 'shotgun_img')
        shotgun_img = pygame.transform.scale(shotgun_img, (20, 20))

        player_rect: pygame.Rect = self.player.get_rect()

        # 총알이 플레이어을 중앙 위에 생기도록 설정
        img_rect = shotgun_img.get_rect()
        img_rect.bottom = player_rect.top
        img_rect.centerx = player_rect.centerx

        speed = StateManager.get_state('bullet', 'speed')
        boundary_rect = StateManager.get_state(
            'stage2', 'entity_boundary')

        for i in range(NUM_OF_BULLET):
            delta_pos = Vector2((5, 0))
            delta_pos.rotate_ip(360*i/NUM_OF_BULLET)
            new_pos = (Vector2(player_rect.center)+delta_pos)[:]
            new_rect = img_rect.copy()
            new_rect.center = new_pos

            new_bullet = Bullet(
                pos=new_rect.topleft,
                img=shotgun_img,
                speed=(speed*delta_pos.normalize())[:],
                boundary_rect=boundary_rect,
                power=self.power
            )
            new_bullet.add_event_listener(
                'delete', self.delete_bullet, new_bullet)
            self.bullets.add_entity(new_bullet)

    def delete_bullet(self, bullet):
        '''
        bullet을 제거한다
        '''
        self.bullets.remove_entity(bullet)

    def _render_skill_info_list(self):
        shotgun_img: pygame.Surface = StateManager.get_state(
            'bullet', 'shotgun_img')
        shotgun_img = pygame.transform.scale(shotgun_img, (50, 50))

        if self.timer.time > 0:  # 비활성화 표시
            temp = pygame.Surface((50, 50), pygame.SRCALPHA)
            temp.fill(self.COLOR_DEACTIVATED)
            shotgun_img.blit(temp, (0, 0))

            cooltime_text = render_text(
                f'{self.timer.time}', StateManager.get_state('global', 'text_color'), 16)
            blit_item(shotgun_img, cooltime_text, bottomright=(50, 50))

        other = super()._render_skill_info_list()
        other.append(shotgun_img)
        return other
