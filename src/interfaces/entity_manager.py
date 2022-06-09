'''
entity_managers
'''

# 모든 manager의 코드가 동일


class EntityManager():
    '''
    엔티티를 관리한다
    '''

    def __init__(self):
        self.array = []
        self.to_delete = set()

    def clear_entities(self):
        self.array.clear()
        self.to_delete.clear()

    def add_entity(self, entity):
        self.array.append(entity)

    def remove_entity(self, entity):
        '이 함수 호출시 제거되지 않고 update 호출 시 한 번에 제거된다'
        self.to_delete.add(entity)

    def add_entities(self, list_entities):
        for entity in list_entities:
            self.array.append(entity)

    def remove_entities(self, list_entities):
        '이 함수 호출시 제거되지 않고 update 호출 시 한 번에 제거된다'
        for entity in list_entities:
            self.to_delete.add(entity)

    def update(self):
        for entity in self.to_delete:
            try:
                self.array.remove(entity)
            except ValueError:
                print("ValueError")
                print(entity)
                exit(1)
        self.to_delete.clear()


class EntityManagerFactory():
    entity_managers: dict[str, EntityManager] = {}

    @classmethod
    def get_manager(cls, name: str):
        if not name in cls.entity_managers:
            cls.entity_managers[name] = EntityManager()
        return cls.entity_managers[name]

    @classmethod
    def clear_all_managers(cls):
        cls.entity_managers.clear()
