'아이템을 소환하는 클래스를 정의한다'

import random

from ...interfaces.entity_manager import EntityManagerFactory
from ...interfaces.game_state import StateManager
from ...interfaces.timer import ManualTimer, TimerManager
from ..sprites.item import Item


class ItemSummoner():
    'interface ItemSummoner'

    def __init__(self):
        self.items = EntityManagerFactory.get_manager('item')

    def summon(self):
        pass


class ItemSummonerDecorator(ItemSummoner):
    'interface WeaponDecorator'

    def __init__(self, summoner: ItemSummoner) -> None:
        super().__init__()
        self._summoner = summoner

    def summon(self):
        self._summoner.summon()


class DefaultStage1ItemSummoner(ItemSummoner):
    '체력을 채워주는 아이템 소환'

    def __init__(self, cooltime_range: tuple[int, int], heal: int):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_stage1_item_summoner')

        self.cooltime_range = cooltime_range
        self.heal = heal

    def summon(self):
        '''
        새로운 아이템을 생성한다
        '''

        if self.timer.time <= 0:
            self.make_item()
            self.timer.time = random.randint(*self.cooltime_range)

    def make_item(self):

        # get config
        offset = StateManager.get_state('item', 'item_offset_width')
        screen_width = StateManager.get_state('global', 'screen_width')
        item_imgs = StateManager.get_state('item', 'imgs')

        new_item = Item(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=item_imgs[random.randint(0, len(item_imgs)-1)],
            speed=(0, StateManager.get_state('item', 'speed')),
            boundary_rect=StateManager.get_state(
                'stage1', 'entity_boundary'),
            heal=self.heal
        )
        new_item.add_event_listener('delete', self.delete_item, new_item)
        self.items.add_entity(new_item)

    def delete_item(self, item):
        self.items.remove_entity(item)


class DefaultStage2ItemSummoner(ItemSummoner):
    '체력을 채워주는 아이템 소환'

    def __init__(self, cooltime_range: tuple[int, int], heal: int):
        super().__init__()
        self.timer = ManualTimer()
        self.timer.set_timeout(0)
        manager = TimerManager()
        manager.set_manual_timer(self.timer, 'default_stage2_item_summoner')

        self.cooltime_range = cooltime_range
        self.heal = heal

    def summon(self):
        '''
        새로운 아이템을 생성한다
        '''

        if self.timer.time <= 0:
            self.make_item()
            self.timer.time = random.randint(*self.cooltime_range)

    def make_item(self):

        # get config
        offset = StateManager.get_state('item', 'item_offset_width')
        screen_width = StateManager.get_state(
            'stage2', 'entity_boundary').width
        item_imgs = StateManager.get_state('item', 'imgs')

        new_item = Item(
            pos=(random.randint(offset, screen_width-offset), 0),
            img=item_imgs[random.randint(0, len(item_imgs)-1)],
            speed=(0, StateManager.get_state('item', 'speed')),
            boundary_rect=StateManager.get_state(
                'stage2', 'entity_boundary'),
            heal=self.heal
        )
        new_item.add_event_listener('delete', self.delete_item, new_item)
        self.items.add_entity(new_item)

    def delete_item(self, item):
        self.items.remove_entity(item)
