from __future__ import annotations
from typing import Dict, Type, List
from domain.event_system.event_system import EventSystem
from domain.math.vector2 import Vector2
from uuid import UUID, uuid4

from src.domain.shapes.line import Line


class WorldObjectComponent:

    def __init__(self, owner: WorldObject, id: UUID, event_system: EventSystem):
        self.__owner = owner
        self.__id = id

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def owner(self) -> WorldObject:
        return self.__owner

    def on_init(self):
        pass

    def draw(self) -> List[Line] | None:
        pass

    def update(self):
        pass


class WorldObject:
    """
    An arbitrary entity that has a position, a scale and an orientation in the world
    Its behaviour is defined by the components that it have
    """

    def __init__(self, id: UUID, event_system: EventSystem, position: Vector2 = Vector2(0, 0), scale: Vector2 = Vector2(1, 1), rotation: float = 0.0):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.__registered_components: Dict[UUID, WorldObjectComponent] = dict()
        self.__event_system = event_system
        self.__id = id

    def add_component(self, cp: Type[WorldObjectComponent]) -> WorldObjectComponent:
        uuid = uuid4()
        component = cp(self, uuid, self.__event_system)
        component.on_init()
        self.__registered_components[uuid] = component
        return component

    def remove_component(self, cp_id: UUID):
        if cp_id in self.__registered_components:
            del self.__registered_components[cp_id]

    def get_component(self, cp_id: UUID) -> WorldObjectComponent:
        if cp_id in self.__registered_components:
            return self.__registered_components[cp_id]
        else:
            raise RuntimeError('Component id not found')

    def update(self):
        for cp in self.__registered_components.values():
            cp.update()

    def draw(self) -> List[Line]:
        lines = list()
        for cp in self.__registered_components.values():
            cp_lines = cp.draw()
            if cp_lines is not None:
                lines = lines + cp_lines
        return lines

    @property
    def id(self) -> UUID:
        return self.__id
