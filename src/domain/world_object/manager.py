from domain.world_object.object import WorldObject
from uuid import UUID, uuid4
from typing import Dict, List
from src.domain.event_system.event_system import EventSystem
from src.domain.shapes.line import Line


class WorldObjectManager:

    def __init__(self, event_system: EventSystem) -> None:
        self.__event_system = event_system
        self.__registered_objects: Dict[UUID, WorldObject] = dict()

    def create(self) -> WorldObject:
        uuid = uuid4()
        object = WorldObject(uuid, self.__event_system)
        return object

    def remove(self, id: UUID):
        if id in self.__registered_objects:
            del self.__registered_objects[id]

    def get(self, id: UUID):
        if id in self.__registered_objects:
            return self.__registered_objects[id]
        else:
            raise RuntimeError('Failed to find world object')

    def update(self):
        for world_obj in self.__registered_objects.values():
            world_obj.update()

    def draw(self) -> List[Line]:
        lines: List[Line] = list()
        for world_obj in self.__registered_objects.values():
            lines = lines + world_obj.draw()
        return lines
