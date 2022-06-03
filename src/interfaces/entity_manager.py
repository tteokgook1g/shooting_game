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

    def clear_entities(self):
        self.array.clear()

    def add_entity(self, entity):
        self.array.append(entity)

    def remove_entity(self, entity):
        self.array.remove(entity)

    def add_entities(self, list_entities):
        for entity in list_entities:
            self.array.append(entity)

    def remove_entities(self, list_entities):
        for entity in list_entities:
            self.array.remove(entity)


class EntityManagerFactory():
    entity_managers: dict[str, EntityManager] = {}

    @classmethod
    def get_manager(cls, name: str):
        if not name in cls.entity_managers:
            cls.entity_managers[name] = EntityManager()
        return cls.entity_managers[name]
